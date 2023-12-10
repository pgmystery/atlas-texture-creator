import os
import shutil
from pathlib import Path
from typing import overload
from PySide6.QtCore import Signal, QObject, Slot, QRunnable
from PySide6.QtWidgets import QInputDialog, QMessageBox, QFileDialog

from atlas_texture_creator import AtlasManager, AtlasCollection, AtlasTexture, AtlasTextureModel
from atlas_texture_creator.atlas_collection import AtlasCollectionTextureStore
from atlas_texture_creator_gui.Window.GenerateAtlasWindow import GenerateAtlasWindow, GenerateAtlasReturnType
from atlas_texture_creator_gui.components.Window import ProgressDialog
from atlas_texture_creator_gui.handlers.CollectionCacheHandler import CollectionCacheHandler, CollectionCache
from atlas_texture_creator_gui.main import AtlasTextureCreatorGUI
from atlas_texture_creator_gui.utils.image_format import get_supported_image_formats


class AddTexturesToCollectionWorker(QRunnable):
    def __init__(
        self,
        file_paths: list[str],
        cache_collection: CollectionCache,
        collection: AtlasCollection,
        atlas_textures: list[AtlasTexture],
        atlas_manager: AtlasManager,
        progress_dialog: ProgressDialog,
    ):
        super().__init__()

        self.file_paths = file_paths
        self.cache_collection = cache_collection
        self.collection = collection
        self.atlas_textures = atlas_textures
        self.atlas_manager = atlas_manager
        self.progress_dialog = progress_dialog

    def run(self):
        for old_file_path in self.file_paths:
            file_path = self.cache_collection.add_texture(old_file_path)
            atlas_texture_model = AtlasTextureModel(
                label=file_path.stem,
                path=Path(file_path),
            )
            atlas_texture = self.collection.add_texture(atlas_texture_model)
            self.atlas_textures.append(atlas_texture)
            self.atlas_manager.add_texture(self.cache_collection.collection_name, atlas_texture)
            self.progress_dialog.step()
        self.progress_dialog.close_signal.emit()


class ExportTexturesWorker(QRunnable):
    def __init__(
        self,
        textures: AtlasCollectionTextureStore,
        export_dir: str,
        progress_dialog: ProgressDialog,
    ):
        super().__init__()

        self.textures = textures
        self.export_dir = export_dir
        self.progress_dialog = progress_dialog

    def run(self):
        for texture in self.textures:
            f = Path(texture.img_path)
            column_str = str(texture.column)
            row_str = str(texture.row)
            new_file_name = f"{column_str},{row_str},{f.name}"
            new_file_path = os.path.join(self.export_dir, new_file_name)
            shutil.copy(texture.img_path, new_file_path)
            self.progress_dialog.step()
        self.progress_dialog.close_signal.emit()


class AtlasManagerHandler(QObject):
    on_load_collections = Signal(list)
    on_current_collection_changed = Signal(AtlasCollection)
    on_collection_created = Signal(AtlasCollection)
    on_collection_deleted = Signal(str)
    on_textures_added = Signal(AtlasCollection, list)

    def __init__(self, app: AtlasTextureCreatorGUI, cache_dir: str):
        super().__init__(app)
        self.app = app
        self.atlas_manager = AtlasManager()
        self._current_collection: AtlasCollection | None = None

        self._collection_cache_handler = CollectionCacheHandler(cache_dir)

    def load_collections(self):
        collections = self.collections()
        self.on_load_collections.emit(collections)

        if len(collections) > 0 and self.current_collection is None:
            self.current_collection = collections[0]

    def collections(self):
        return self.atlas_manager.list_collections()

    @overload
    def current_collection(self, collection: AtlasCollection): ...

    @overload
    def current_collection(self, collection_name: str): ...

    @overload
    def current_collection(self, collection_name: None): ...

    @property
    def current_collection(self):
        return self._current_collection

    @current_collection.setter
    def current_collection(self, collection: AtlasCollection | str | None):
        if collection is None:
            collections = self.atlas_manager.list_collections()
            if len(collections) > 0:
                self._current_collection = collections[0]
            else:
                self._current_collection = None
        elif isinstance(collection, AtlasCollection):
            if self._current_collection == collection.name:
                return

            self._current_collection = collection
        elif isinstance(collection, str):
            if self._current_collection == collection:
                return

            collection = self.atlas_manager.load_collection(collection)
            self._current_collection = collection
        else:
            raise TypeError("Bad collection type")

        self.on_current_collection_changed.emit(collection)

    def create_collection(self) -> AtlasCollection | None:
        collection_name, is_ok = QInputDialog.getText(
            self.app.activeWindow(),
            "Create Atlas-Collection",
            "Enter your new Atlas-Collection name"
        )

        if is_ok and len(collection_name) > 0:
            atlas_collection = self.atlas_manager.create_collection(collection_name)
            self.on_collection_created.emit(atlas_collection)
            self.current_collection = atlas_collection

            return atlas_collection

    def delete_collection(self, collection_name: str):
        answer = QMessageBox.question(
            self.app.activeWindow(),
            "Delete Collection?",
            f"Do you really want to delete the collection '{collection_name}'?"
            f"\nAll attached textures also getting deleted!",
            QMessageBox.Yes | QMessageBox.No
        )
        if answer == QMessageBox.Yes:
            self.atlas_manager.delete_collection(collection_name)
            cache_collection = self._collection_cache_handler(collection_name)
            cache_collection.delete()
            self.on_collection_deleted.emit(collection_name)

            if self.current_collection is not None and self.current_collection.name == collection_name:
                self.current_collection = None

    def delete_current_collection(self):
        self.delete_collection(self.current_collection.name)

    def generate_current_collection_to_atlas(self):
        if self.current_collection is not None:
            self.generate_atlas(self.current_collection)

    @overload
    def generate_atlas(self, collection: AtlasCollection): ...

    @overload
    def generate_atlas(self, collection: str): ...

    def generate_atlas(self, collection: AtlasCollection | str):
        def generate_atlas_callback(options: GenerateAtlasReturnType):
            save_path = options.file_path
            save_path_dir = os.path.dirname(save_path)
            save_path_obj = Path(save_path)
            texture_coords_path = os.path.join(save_path_dir, f"{save_path_obj.stem}.json")

            img, texture_coords = collection.generate_atlas(options)

            img.save(save_path)
            with open(texture_coords_path, 'w') as f:
                f.write(texture_coords.json())

        if isinstance(collection, str):
            collection = self.atlas_manager.load_collection(collection)
        elif not isinstance(collection, AtlasCollection):
            raise TypeError("Bad collection type")

        self.generate_atlas_window = GenerateAtlasWindow(generate_atlas_callback)
        self.generate_atlas_window.show()

    def add_texture_to_current_collection(self):
        if self.current_collection is not None:
            self.add_texture_to_collection(self.current_collection)

    def add_texture_to_collection(self, collection: AtlasCollection):
        def _add_texture_to_collection():
            worker = AddTexturesToCollectionWorker(
                file_paths=file_paths,
                cache_collection=cache_collection,
                collection=collection,
                atlas_textures=atlas_textures,
                atlas_manager=self.atlas_manager,
                progress_dialog=progress_dialog
            )
            self.app.thread_pool.start(worker)

        window = self.app.activeWindow()
        texture_open_dialog = QFileDialog(window)
        texture_open_dialog_images_filter = f"Images ({get_supported_image_formats()})"

        file_paths = texture_open_dialog.getOpenFileNames(
            window,
            "Select the texture to add",
            "",
            texture_open_dialog_images_filter,
            texture_open_dialog_images_filter
        )[0]

        if len(file_paths) > 0:
            atlas_textures = []
            cache_collection = self._collection_cache_handler(collection.name)

            progress_dialog = ProgressDialog(
                label="Adding Textures...",
                max=len(file_paths),
                parent=self.app.window
            )
            progress_dialog.on_open.connect(_add_texture_to_collection)
            progress_dialog.show()

            self.on_textures_added.emit(collection, atlas_textures)

    def export_textures_of_current_collection(self):
        if self.current_collection is not None:
            self.export_textures_of_collection(self.current_collection)

    @overload
    def export_textures_of_collection(self, collection: str): ...

    @overload
    def export_textures_of_collection(self, collection: AtlasCollection): ...

    def export_textures_of_collection(self, collection: AtlasCollection | str):
        @Slot()
        def _export_textures_of_collection():
            export_textures_worker = ExportTexturesWorker(
                textures=textures,
                export_dir=export_dir,
                progress_dialog=progress_dialog,
            )
            self.app.thread_pool.start(export_textures_worker)

        if isinstance(collection, str):
            collection = self.atlas_manager.load_collection(collection)
        elif not isinstance(collection, AtlasCollection):
            raise TypeError("Bad collection type")

        window = self.app.activeWindow()
        self.export_textures_dialog = QFileDialog(window)

        dir_path = self.export_textures_dialog.getExistingDirectory(
            window,
            "Select the directory to export the textures",
            "",
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks,
        )

        if dir_path:
            export_dir = os.path.join(dir_path, collection.name)
            if not os.path.exists(export_dir):
                os.makedirs(export_dir)

            textures = collection.textures

            progress_dialog = ProgressDialog(
                label="Export Textures...",
                max=len(textures),
                parent=self.app.window
            )
            progress_dialog.on_open.connect(_export_textures_of_collection)
            progress_dialog.show()

    def replace_texture_of_current_collection(self, new_texture: AtlasTexture):
        if self.current_collection is not None:
            self.replace_texture_of_collection(self.current_collection, new_texture)

    def replace_texture_of_collection(self, collection: AtlasCollection | str, new_texture: AtlasTexture):
        if isinstance(collection, str):
            collection = self.atlas_manager.load_collection(collection)
        elif not isinstance(collection, AtlasCollection):
            raise TypeError("Bad collection type")

        cache_collection = self._collection_cache_handler(collection.name)

        old_texture = collection.get_texture(new_texture.row, new_texture.column)
        old_texture_path = old_texture.path
        new_texture_path = str(new_texture.path)
        if old_texture_path != new_texture_path:
            number_of_texture_path_in_use = len(list(filter(
                lambda texture: texture.path == old_texture.path,
                collection.textures
            )))
            old_texture_name = Path(old_texture_path).name
            new_texture.path = cache_collection.replace_texture(
                old_texture_name,
                new_texture_path,
                number_of_texture_path_in_use=number_of_texture_path_in_use
            )

        self.atlas_manager.update_texture(collection.name, new_texture)
        collection.update_texture(
            row=new_texture.row,
            column=new_texture.column,
            new_texture_model=AtlasTextureModel(**dict(new_texture)),
        )
