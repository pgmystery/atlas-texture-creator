from pathlib import Path

import pytest
from PIL.Image import Image

from atlas_texture_creator import AtlasCollection, AtlasTexture, AtlasTextureModel
from atlas_texture_creator.atlas_collection import GenerateAtlasTextureCoords
from atlas_texture_creator.types import AtlasGridItem, GenerateAtlasOptions, GenerateAtlasCoordTexture, \
    GenerateAtlasOptionsSize


def _mock_data_dir() -> Path:
    return Path(".mock")


mock_dir = _mock_data_dir()
test_image_file_path = mock_dir / "white.png"


def test_create_atlas_collection():
    atlas_collection = AtlasCollection(
        name="test",
    )

    assert isinstance(atlas_collection, AtlasCollection)


def test_add_texture_to_a_collection():
    atlas_collection = AtlasCollection("test")
    atlas_texture_model = AtlasTextureModel(
        path=test_image_file_path,
        label="texture",
    )

    atlas_texture = atlas_collection.add_texture(atlas_texture_model)

    assert atlas_texture == atlas_collection.get_texture(0, 0)


def test_get_texture(atlas_collection: AtlasCollection, atlas_texture_model: AtlasTextureModel):
    atlas_texture = atlas_collection.add_texture(atlas_texture_model)

    assert atlas_collection.get_texture(row=atlas_texture.row, column=atlas_texture.column) == atlas_texture


def test_get_texture_index_error(atlas_collection: AtlasCollection):
    with pytest.raises(IndexError):
        atlas_collection.get_texture(row=1, column=100)


def test_load_texture_to_a_collection():
    atlas_collection = AtlasCollection("test")
    atlas_texture = AtlasTexture(
        path=test_image_file_path,
        label="texture",
    )

    atlas_collection.load_texture(atlas_texture)

    assert atlas_texture == atlas_collection.get_texture(0, 0)


def test_load_multiple_textures_to_a_collection():
    """
    grid length: 10

    0-0 | 1-0 | 2-0
    0-1 | 1-1 | 2-1
    0-2 | 1-2 | 2-2
    0-3

    """

    texture_coords = [
        AtlasGridItem(column=0, row=0),
        AtlasGridItem(column=0, row=1),
        AtlasGridItem(column=0, row=2),
        AtlasGridItem(column=0, row=3),
        AtlasGridItem(column=1, row=0),
        AtlasGridItem(column=1, row=1),
        AtlasGridItem(column=1, row=2),
        AtlasGridItem(column=2, row=0),
        AtlasGridItem(column=2, row=1),
        AtlasGridItem(column=2, row=2),
    ]

    atlas_collection = AtlasCollection("test")

    textures = []
    for i in range(0, len(texture_coords)):
        atlas_texture = AtlasTexture(
            path=test_image_file_path,
            label=f"texture {i}",
        )
        textures.append(atlas_texture)

    atlas_collection.load_textures(textures)

    assert len(atlas_collection) == len(texture_coords)

    counter = 0
    for texture in atlas_collection:
        assert texture.get_coord() == texture_coords[counter]
        counter += 1


def test_update_texture_in_collection():
    old_texture_label = "texture"
    new_texture_label = "new_texture"

    atlas_collection = AtlasCollection("test")

    old_atlas_texture_model = AtlasTextureModel(
        path=test_image_file_path,
        label=old_texture_label,
    )

    new_atlas_texture_model = AtlasTextureModel(
        path=test_image_file_path,
        label=new_texture_label,
    )

    atlas_collection.add_texture(old_atlas_texture_model)

    assert atlas_collection.get_texture(0, 0).label == old_texture_label

    atlas_collection.update_texture(row=0, column=0, new_texture_model=new_atlas_texture_model)

    assert atlas_collection.get_texture(0, 0).label == new_texture_label


def test_update_texture_in_collection_with_index_error(
    atlas_collection: AtlasCollection,
    atlas_texture_model: AtlasTextureModel,
):
    new_texture_label = "new_texture"

    new_atlas_texture = AtlasTextureModel(
        path=test_image_file_path,
        label=new_texture_label,
    )

    atlas_collection.add_texture(atlas_texture_model)

    with pytest.raises(IndexError):
        atlas_collection.update_texture(row=1, column=1, new_texture_model=new_atlas_texture)


def test_generate_atlas_without_options_and_no_textures(atlas_collection: AtlasCollection):
    atlas_image, texture_coords = atlas_collection.generate_atlas()

    assert isinstance(atlas_image, Image)
    assert isinstance(texture_coords, GenerateAtlasTextureCoords)


def test_generate_atlas_without_options(atlas_collection: AtlasCollection, atlas_texture_model: AtlasTextureModel):
    textures_count = 10

    texture_labels = [atlas_texture_model.label]

    atlas_collection.add_texture(atlas_texture_model)

    for i in range(0, textures_count):
        atlas_collection_model_tmp = atlas_texture_model.copy()

        label = f"{atlas_collection_model_tmp.label} {i}"
        atlas_collection_model_tmp.label = label

        atlas_collection.add_texture(atlas_collection_model_tmp)
        texture_labels.append(label)

    atlas_image, texture_coords = atlas_collection.generate_atlas()

    assert isinstance(atlas_image, Image)
    assert isinstance(texture_coords, GenerateAtlasTextureCoords)

    for label, atlas_texture_coord in texture_coords:
        assert label in texture_labels
        assert isinstance(atlas_texture_coord, GenerateAtlasCoordTexture)


def test_generate_atlas_with_options_and_no_textures(atlas_collection: AtlasCollection):
    atlas_option_size_width = 69
    atlas_option_size_height = 420

    atlas_option_size = GenerateAtlasOptionsSize(
        width=atlas_option_size_width,
        height=atlas_option_size_height,
    )
    atlas_options = GenerateAtlasOptions(
        lock_size=atlas_option_size
    )
    atlas_image, texture_coords = atlas_collection.generate_atlas(atlas_options)

    assert isinstance(atlas_image, Image)
    assert isinstance(texture_coords, GenerateAtlasTextureCoords)


def test_generate_atlas_with_options(atlas_collection: AtlasCollection, atlas_texture_model: AtlasTextureModel):
    textures_count = 10
    atlas_option_size_width = 69
    atlas_option_size_height = 420

    atlas_option_size = GenerateAtlasOptionsSize(
        width=atlas_option_size_width,
        height=atlas_option_size_height,
    )
    atlas_options = GenerateAtlasOptions(
        lock_size=atlas_option_size
    )

    texture_labels = [atlas_texture_model.label]

    atlas_collection.add_texture(atlas_texture_model)

    for i in range(0, textures_count):
        atlas_collection_model_tmp = atlas_texture_model.copy()

        label = f"{atlas_collection_model_tmp.label} {i}"
        atlas_collection_model_tmp.label = label

        atlas_collection.add_texture(atlas_collection_model_tmp)
        texture_labels.append(label)

    atlas_image, texture_coords = atlas_collection.generate_atlas(atlas_options)

    assert isinstance(atlas_image, Image)
    assert isinstance(texture_coords, GenerateAtlasTextureCoords)

    for label, atlas_texture_coord in texture_coords:
        assert label in texture_labels
        assert isinstance(atlas_texture_coord, GenerateAtlasCoordTexture)
        assert atlas_texture_coord.width == atlas_option_size_width
        assert atlas_texture_coord.height == atlas_option_size_height
