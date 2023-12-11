import os
from pathlib import Path
from typing import Callable

import pydantic
import pytest
from decorator import decorator

from atlas_texture_creator import AtlasManager, AtlasManagerConfig, AtlasCollection, AtlasTexture
from tests.conftest import sqlite_file_path, test_image_file_path, test_image_file_path2


def delete_file_after_done(file_path: str):
    def deco(function: Callable):
        def wrapper(callback: Callable, *args, **kwargs):
            with DeleteFile(file_path):
                return callback(*args, **kwargs)
        return decorator(wrapper, function)
    return deco


def test_create_atlas_manager():
    with DeleteFile(AtlasManager.sqlite_file):
        atlas_manager = AtlasManager()
        assert atlas_manager
        atlas_manager.close_all_connections()


@delete_file_after_done(sqlite_file_path)
def test_create_atlas_manager_with_options(atlas_manager_config: AtlasManagerConfig):
    atlas_manager = AtlasManager(atlas_manager_config)
    assert atlas_manager
    atlas_manager.close_all_connections()


def test_create_collection_from_string(atlas_manager_with_config: AtlasManager):
    atlas_collection = atlas_manager_with_config.create_collection("test")

    assert isinstance(atlas_collection, AtlasCollection)


def test_create_collection_with_empty_name(atlas_manager_with_config: AtlasManager):
    try:
        atlas_manager_with_config.create_collection("")
    except pydantic.error_wrappers.ValidationError as exc:
        assert "value_error.any_str.min_length" == exc.errors()[0]['type']


def test_create_collection_from_object(atlas_manager_with_config: AtlasManager):
    collection = AtlasCollection(name="test")
    atlas_collection = atlas_manager_with_config.create_collection(collection)

    assert collection == atlas_collection


def test_load_collection(atlas_manager_with_config: AtlasManager):
    COLLECTION_NAME = "test"

    atlas_collection = atlas_manager_with_config.create_collection(COLLECTION_NAME)
    atlas_collection2 = atlas_manager_with_config.load_collection(COLLECTION_NAME)

    assert atlas_collection2 is not None
    assert atlas_collection == atlas_collection2


def test_update_collection(atlas_manager_with_config: AtlasManager):
    old_collection_name = "old"
    new_collection_name = "new"

    old_collection = AtlasCollection(name=old_collection_name)
    new_collection = AtlasCollection(name=new_collection_name)

    atlas_collection = atlas_manager_with_config.create_collection(old_collection)

    assert atlas_collection == old_collection
    assert atlas_collection.name == old_collection_name

    atlas_collection = atlas_manager_with_config.update_collection(old_collection_name, new_collection)

    assert atlas_collection.dict() == new_collection.dict()
    assert atlas_collection.name == new_collection_name


def test_delete_collection(atlas_manager_with_config: AtlasManager):
    COLLECTION_NAME = "test"

    atlas_collection = atlas_manager_with_config.create_collection(COLLECTION_NAME)
    atlas_collection2 = atlas_manager_with_config.load_collection(COLLECTION_NAME)

    assert atlas_collection2 is not None
    assert atlas_collection == atlas_collection2

    atlas_manager_with_config.delete_collection(atlas_collection.name)

    assert atlas_manager_with_config.load_collection(COLLECTION_NAME) is None


def test_list_collections(atlas_manager_with_config: AtlasManager):
    COLLECTION_NAME = "test"
    CREATE_COLLECTIONS = 3

    collections = atlas_manager_with_config.list_collections()

    assert type(collections) is list
    assert len(collections) == 0

    collection_names = []
    for i in range(CREATE_COLLECTIONS):
        new_collection_name = COLLECTION_NAME + str(i)
        collection_names.append(new_collection_name)
        atlas_manager_with_config.create_collection(new_collection_name)

    collections = atlas_manager_with_config.list_collections()

    assert type(collections) is list
    assert len(collections) == CREATE_COLLECTIONS
    for collection_name in collections:
        collection = atlas_manager_with_config.load_collection(collection_name)
        assert collection.name in collection_names


def test_add_texture(atlas_manager_with_config: AtlasManager):
    COLLECTION_NAME = "test"

    atlas_collection = atlas_manager_with_config.create_collection(COLLECTION_NAME)
    atlas_texture = AtlasTexture(
        path=test_image_file_path,
        label="test",
    )
    atlas_manager_with_config.add_texture(atlas_collection.name, atlas_texture)


def test_load_textures(atlas_manager_with_config: AtlasManager):
    COLLECTION_NAME = "test"

    atlas_collection = atlas_manager_with_config.create_collection(COLLECTION_NAME)
    atlas_texture = AtlasTexture(
        path=test_image_file_path,
        label="test",
    )
    atlas_manager_with_config.add_texture(atlas_collection.name, atlas_texture)

    atlas_textures = atlas_manager_with_config.load_textures(atlas_collection.name)

    assert type(atlas_textures) is list
    assert len(atlas_textures) == 1
    assert atlas_textures[0] == atlas_texture


def test_update_texture(atlas_manager_with_config: AtlasManager):
    COLLECTION_NAME = "test"
    UPDATE_TEXTURE_NAME = "test2"
    UPDATE_TEXTURE_PATH = test_image_file_path2

    atlas_collection = atlas_manager_with_config.create_collection(COLLECTION_NAME)
    atlas_texture = AtlasTexture(
        path=test_image_file_path,
        label="test",
    )
    atlas_manager_with_config.add_texture(atlas_collection.name, atlas_texture)

    atlas_textures = atlas_manager_with_config.load_textures(atlas_collection.name)

    assert type(atlas_textures) is list
    assert len(atlas_textures) == 1
    atlas_texture2 = atlas_textures[0]
    assert atlas_texture2 == atlas_texture

    atlas_texture2.label = UPDATE_TEXTURE_NAME
    atlas_texture2.path = UPDATE_TEXTURE_PATH

    atlas_manager_with_config.update_texture(atlas_collection.name, atlas_texture2)

    atlas_textures = atlas_manager_with_config.load_textures(atlas_collection.name)

    assert type(atlas_textures) is list
    assert len(atlas_textures) == 1
    atlas_texture3 = atlas_textures[0]
    assert atlas_texture3 == atlas_texture2
    assert atlas_texture3.label == UPDATE_TEXTURE_NAME
    assert atlas_texture3.path == UPDATE_TEXTURE_PATH


class DeleteFile:
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

    def __enter__(self):
        return self

    def __exit__(self, _, __, ___):
        if self.file_path.is_file():
            print("REMOVE FILE")
            os.remove(self.file_path)
