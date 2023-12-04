import os
from pathlib import Path
import pytest

from atlas_texture_creator import AtlasTexture, AtlasCollection, AtlasTextureModel, AtlasManager, AtlasManagerConfig, \
    AtlasManagerConfigDB


def mock_data_dir() -> Path:
    return Path(".mock")


mock_dir = mock_data_dir()
test_image_file_path = mock_dir / "white.png"
test_image_file_path2 = mock_dir / "black.png"
sqlite_file_path = f"{str(mock_dir)}/atlas_manager.db"


def create_atlas_texture_model() -> AtlasTextureModel:
    return AtlasTextureModel(
        path=test_image_file_path,
        label="test",
    )


def create_atlas_manager_config() -> AtlasManagerConfig:
    return AtlasManagerConfig(
        db=AtlasManagerConfigDB(sqlite_path=sqlite_file_path)
    )


@pytest.fixture
def atlas_texture_model() -> AtlasTextureModel:
    return create_atlas_texture_model()


@pytest.fixture
def atlas_texture() -> AtlasTexture:
    _atlas_texture_model = create_atlas_texture_model()

    return AtlasTexture(
        **dict(_atlas_texture_model),
        column=0,
        row=0,
    )


@pytest.fixture
def atlas_collection() -> AtlasCollection:
    return AtlasCollection(
        name="test",
    )


@pytest.fixture
def atlas_manager() -> AtlasManager:
    atlas_manager = AtlasManager()

    yield atlas_manager

    atlas_manager.close_all_connections()
    delete_file(atlas_manager.sqlite_file)


@pytest.fixture
def atlas_manager_config() -> AtlasManagerConfig:
    return create_atlas_manager_config()


@pytest.fixture
def atlas_manager_with_config() -> AtlasManager:
    atlas_manager_config = create_atlas_manager_config()
    atlas_manager = AtlasManager(atlas_manager_config)

    yield atlas_manager

    atlas_manager.close_all_connections()
    delete_file(atlas_manager.sqlite_file)


def delete_file(file_path: str):
    f = Path(file_path)

    if f.is_file():
        os.remove(f)
