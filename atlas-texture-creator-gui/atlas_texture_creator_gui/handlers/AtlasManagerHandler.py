from typing import overload
from PySide6.QtCore import Signal, QObject
from PySide6.QtWidgets import QInputDialog, QApplication, QMessageBox

from atlas_texture_creator import AtlasManager, AtlasCollection
from atlas_texture_creator_gui.handlers.CollectionCacheHandler import CollectionCacheHandler


class AtlasManagerHandler(QObject):
    on_load_collections = Signal(list)
    on_current_collection_changed = Signal(AtlasCollection)
    on_collection_created = Signal(AtlasCollection)
    on_collection_deleted = Signal(str)

    def __init__(self, app: QApplication, cache_dir: str):
        super().__init__(app)
        self.app = app
        self.atlas_manager = AtlasManager()
        self._current_collection: AtlasCollection | None = None

        self._collection_cache_handler = CollectionCacheHandler(cache_dir)

    def load_collections(self):
        collections = self.atlas_manager.list_collections()
        self.on_load_collections.emit(collections)

        if len(collections) > 0 and self.current_collection is None:
            self.current_collection = collections[0]

    @overload
    def current_collection(self, collection: AtlasCollection):
        ...

    @overload
    def current_collection(self, collection_name: str):
        ...

    @property
    def current_collection(self):
        return self._current_collection

    @current_collection.setter
    def current_collection(self, collection: AtlasCollection | str):
        if isinstance(collection, AtlasCollection):
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

        if is_ok:
            atlas_collection = self.atlas_manager.create_collection(collection_name)
            self.on_collection_created.emit(atlas_collection)

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

    def delete_current_collection(self):
        self.delete_collection(self.current_collection.name)
