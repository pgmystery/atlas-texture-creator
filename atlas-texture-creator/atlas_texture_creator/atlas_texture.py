from pydantic import FilePath, BaseModel

from atlas_texture_creator.types import AtlasGridItem


class AtlasTextureModel(BaseModel):
    path: FilePath
    label: str


class AtlasTexture(AtlasGridItem, AtlasTextureModel):
    def get_coord(self) -> AtlasGridItem:
        atlas_grid_item = AtlasGridItem(
            column=self.column,
            row=self.row,
        )

        return atlas_grid_item

    def set_coord(self, column: int, row: int):
        self.column = column
        self.row = row

    @property
    def img_path(self):
        return self.path

    def set_img_path(self, path):
        self.path = path

    def get_data(self) -> AtlasTextureModel:
        return AtlasTextureModel(**dict(self))

    def update(self, new_atlas_texture: AtlasTextureModel):
        new_atlas_texture_dict = dict(new_atlas_texture)

        self.__class__.validate(self.__dict__ | new_atlas_texture_dict)
        self.__dict__.update(**new_atlas_texture_dict)
