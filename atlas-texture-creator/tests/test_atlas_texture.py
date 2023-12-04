from pathlib import Path

import pydantic.error_wrappers
import pytest

from atlas_texture_creator import AtlasTexture, AtlasTextureModel
from atlas_texture_creator.types import AtlasGridItem
from tests.conftest import test_image_file_path, mock_dir


def test_create_atlas_texture_instance():
    atlas_texture = AtlasTexture(
        path=test_image_file_path,
        label="test",
    )

    assert isinstance(atlas_texture, AtlasTexture)


def test_create_atlas_texture_with_wrong_path():
    with pytest.raises(pydantic.error_wrappers.ValidationError):
        AtlasTexture(
            path=Path(),
            label="test",
        )


def test_create_atlas_texture_and_set_column_and_row():
    old_column = 0
    old_row = 0
    new_column = 1
    new_row = 2

    atlas_texture = AtlasTexture(
        path=test_image_file_path,
        label="test",
        column=old_column,
        row=old_row,
    )

    atlas_texture_coordinates = atlas_texture.get_coord()

    assert atlas_texture_coordinates.column == old_column
    assert atlas_texture_coordinates.row == old_row

    atlas_texture.set_coord(new_column, new_row)

    assert atlas_texture.column == new_column
    assert atlas_texture.row == new_row


def test_get_data():
    atlas_texture_data = {
        "path": test_image_file_path,
        "label": "test",
    }

    atlas_texture = AtlasTexture(**atlas_texture_data)

    atlas_texture_model = atlas_texture.get_data()

    assert dict(atlas_texture_model) == atlas_texture_data


def test_get_coord():
    column = 0
    row = 0

    atlas_texture_coord = AtlasGridItem(column=column, row=row)
    atlas_texture = AtlasTexture(
        path=test_image_file_path,
        label="test",
        column=column,
        row=row,
    )

    assert atlas_texture.get_coord() == atlas_texture_coord


def test_get_img_path():
    texture_path = test_image_file_path

    atlas_texture = AtlasTexture(
        path=texture_path,
        label="test",
    )

    assert atlas_texture.img_path == texture_path


def test_set_img_path():
    old_texture_path = test_image_file_path
    new_texture_path = mock_dir / "black.png"

    atlas_texture = AtlasTexture(
        path=old_texture_path,
        label="test",
    )

    assert atlas_texture.img_path == old_texture_path

    atlas_texture.set_img_path(new_texture_path)

    assert atlas_texture.img_path == new_texture_path
    assert atlas_texture.path == new_texture_path


def test_update_123(atlas_texture: AtlasTexture):
    new_texture_path = mock_dir / "black.png"
    new_texture_label = "new_test_label"

    atlas_texture_model = AtlasTextureModel(
        path=new_texture_path,
        label=new_texture_label,
    )

    assert atlas_texture.get_data() != atlas_texture_model

    atlas_texture.update(atlas_texture_model)

    assert atlas_texture.get_data() == atlas_texture_model
