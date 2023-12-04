import math
from typing import Iterator

from PIL import Image
from pydantic import BaseModel, Field, Extra

from atlas_texture_creator.atlas_texture import AtlasTexture, AtlasTextureModel
from atlas_texture_creator.types import GenerateAtlasReturnType, GenerateAtlasCoordTexture, \
    GenerateAtlasReturnTypeOut, AtlasGridDirection, GenerateAtlasOptions, AtlasGridItem, Column, Row


class AtlasCollectionModel(BaseModel):
    name: str = Field(unique=True)


class GenerateAtlasTextureCoords:
    def __init__(self, init_data: GenerateAtlasReturnType = None):
        if init_data is None:
            init_data = {}

        self.data: GenerateAtlasReturnType = init_data

    def add_data(self, label: str, data: GenerateAtlasCoordTexture):
        self.data[label] = data

    def json(self):
        return GenerateAtlasReturnTypeOut.parse_obj(self.data).json()

    def __len__(self):
        return len(self.data.keys())

    def __iter__(self):
        for label, atlas_texture_coord in self.data.items():
            yield label, atlas_texture_coord


class AtlasCollectionTextureStore:
    def __init__(self, grid_direction: AtlasGridDirection = "row"):
        self._textures: list[list[AtlasTexture]] = []
        self.grid = AtlasGrid(direction=grid_direction)

        # 1 = self._textures[0][0] = [[1]]  # new array
        # 2 = self._textures[0][1] = [[1, 2]]
        # 3 = self._textures[1][0] = [[1, 2], [3]]  # new array
        # 4 = self._textures[1][1] = [[1, 2], [3, 4]]
        # 5 = self._textures[0][2] = [[1, 2, 5], [3, 4]]
        # 6 = self._textures[2][0] = [[1, 2, 5], [3, 4], [6]]  # new array
        # 7 = self._textures[1][2] = [[1, 2, 5], [3, 4, 7], [6]]
        # 8 = self._textures[2][1] = [[1, 2, 5], [3, 4, 7], [6, 8]]
        # 9 = self._textures[2][2] = [[1, 2, 5], [3, 4, 7], [6, 8, 9]]
        # 10 = self._textures[0][3] = [[1, 2, 5, 10], [3, 4, 7], [6, 8, 9]]
        # 11 = self._textures[3][0] = [[1, 2, 5, 10], [3, 4, 7], [6, 8, 9], [11]]  # new array
        # 12 = self._textures[1][3] = [[1, 2, 5, 10], [3, 4, 7, 12], [6, 8, 9], [11]]
        # 13 = self._textures[3][1] = [[1, 2, 5, 10], [3, 4, 7, 12], [6, 8, 9], [11, 13]]
        # 14 = self._textures[2][3] = [[1, 2, 5, 10], [3, 4, 7, 12], [6, 8, 9, 14], [11, 13]]
        # 15 = self._textures[3][2] = [[1, 2, 5, 10], [3, 4, 7, 12], [6, 8, 9, 14], [11, 13, 15]]
        # 16 = self._textures[3][3] = [[1, 2, 5, 10], [3, 4, 7, 12], [6, 8, 9, 14], [11, 13, 15, 16]]
        # 17 = self._textures[0][4] = [[1, 2, 5, 10, 17], [3, 4, 7, 12], [6, 8, 9, 14], [11, 13, 15, 16]]
        # 18 = self._textures[4][0] = [[1, 2, 5, 10, 17], [3, 4, 7, 12], [6, 8, 9, 14], [11, 13, 15, 16], [18]]  # new array
        # self._textures[self.row_counter][self.column_counter]
        # arrays = row; numbers in array = column
        # column = 0 = new array

    def add(self, texture: AtlasTexture) -> AtlasGridItem:
        grid_item = self.grid.add()

        texture.set_coord(column=grid_item.column, row=grid_item.row)
        self._store_texture(texture, column=grid_item.column, row=grid_item.row)

        return grid_item

    def replace(self, texture_model: AtlasTextureModel, row: Row, column: Column):
        atlas_texture = self._textures[column][row]
        atlas_texture.update(texture_model)

    def _store_texture(self, texture: AtlasTexture, row: Row, column: Column):
        texture.set_coord(column=column, row=row)

        if len(self._textures) == column:
            self._textures.append([])

        self._textures[column].append(texture)

    def get(self, row: Row, column: Column):
        return self._textures[column][row]

    def column(self, column: Column):
        return self._textures[column]

    def row(self, row: Row):
        row_list = []

        for column in self._textures:
            texture = column[row]
            row_list.append(texture)

        return row_list

    def __iter__(self):
        # COLUMNS
        for column in self._textures:
            for item in column:
                yield item

        # ROWS: # TODO: NOT WORKING
        # counter = 0
        # all_items_yield = False
        # while not all_items_yield:
        #     for row in self._textures:
        #         try:
        #             yield row[counter]
        #         except IndexError:
        #             all_items_yield = True
        #             break
        #     counter += 1

        # square_number = math.ceil(math.sqrt(self._store_length))
        #
        # for column in range(square_number):
        #     for row in range(square_number):
        #         try:
        #             yield self.get(row=row, column=column)
        #         except IndexError:
        #             break

    def __getitem__(self, item):
        return self._textures[item]

    def __len__(self):
        return len(self.grid)

    def _coord_flip(self):
        self._add_to_column = 0 if self._add_to_column == 1 else 1

    def _reset_add_to_column(self):
        self._add_to_column = 0

    def __eq__(self, other: "AtlasCollectionTextureStore"):
        if len(self) != len(other):
            return False

        for texture in self:
            try:
                other_texture = other.get(texture.row, texture.column)
            except IndexError:
                return False

            if texture != other_texture:
                return False

        return True


class AtlasGrid:
    def __init__(self, direction: AtlasGridDirection):
        self.direction = direction
        self.squares = 0
        self.column = 0
        self.row = 0
        self.offset = 0

    def add(self) -> AtlasGridItem:
        if self._calc_square():
            row = column = self.squares

            self._set_next_square()
        else:
            row = column = self.offset

            if self.direction == "row":
                if self.column == self.row:
                    self.row += 1
                    row = self.squares
                elif self.column < self.row:
                    self.column += 1
                    column = self.squares
                    self.offset += 1
            elif self.direction == "column":
                if self.column == self.row:
                    self.column += 1
                    column = self.squares
                elif self.row < self.column:
                    self.row += 1
                    row = self.squares
                    self.offset += 1

        item = AtlasGridItem(
            column=column,
            row=row,
        )

        return item

    def _calc_square(self) -> bool:
        length = len(self) + 1
        l_sqrt = math.sqrt(length)
        is_integer = l_sqrt.is_integer()

        return is_integer

    def _set_next_square(self):
        self.squares += 1
        self.offset = 0
        self.row = 0
        self.column = 0

    def __len__(self):
        length = (self.squares * self.squares) + self.row + self.column

        return length


class AtlasCollection(AtlasCollectionModel, extra=Extra.allow):
    def __init__(self, name: "AtlasCollection.name"):
        super().__init__(
            name=name,
        )
        self.texture_store = AtlasCollectionTextureStore()

    def add_texture(self, texture_model: AtlasTextureModel) -> AtlasTexture:
        atlas_texture = AtlasTexture(
            **dict(texture_model),
        )
        grid_item = self.texture_store.add(atlas_texture)

        atlas_texture.set_coord(column=grid_item.column, row=grid_item.row)

        return atlas_texture

    def load_texture(self, texture: AtlasTexture):
        self.texture_store.add(texture)

    def load_textures(self, textures: list[AtlasTexture]):
        for texture in textures:
            self.load_texture(texture)

    def get_texture(self, row: Row, column: Column) -> AtlasTexture:
        return self.texture_store.get(row=row, column=column)

    @property
    def textures(self) -> AtlasCollectionTextureStore:
        return self.texture_store

    def update_texture(self, row: Row, column: Column, new_texture_model: AtlasTextureModel):
        self.texture_store.replace(new_texture_model, row=row, column=column)

    def generate_atlas(self, options: GenerateAtlasOptions = None) -> tuple[Image.Image, GenerateAtlasTextureCoords]:
        textures_coord = GenerateAtlasTextureCoords()
        atlas_width = 0
        atlas_height = 0
        square_number = math.ceil(math.sqrt(len(self.texture_store)))
        lock_texture_width = None
        lock_texture_height = None

        if options is not None and options.lock_size:
            lock_texture_width = options.lock_size.width
            lock_texture_height = options.lock_size.height

        atlas = Image.new(mode="RGBA", size=(0, 0))

        for row in range(square_number):
            column_width = 0
            column_height = 0
            column_imgs = []

            for column in range(square_number):
                try:
                    texture = self.texture_store.get(row=row, column=column)
                except IndexError:
                    continue
                img = Image.open(texture.img_path)

                if lock_texture_width is not None or lock_texture_height is not None:
                    new_img_width = lock_texture_width or img.width
                    new_img_height = lock_texture_height or img.height
                    img = img.resize((new_img_width, new_img_height))

                img_width, img_height = img.size

                if img_width > column_width:
                    column_width = img_width
                column_height += img_height

                column_imgs.append({
                    "label": texture.label,
                    "img": img,
                })

            offset_x = atlas_width
            offset_y = 0

            atlas_width += column_width
            if column_height > atlas_height:
                atlas_height = column_height

            new_atlas = Image.new("RGBA", size=(atlas_width, atlas_height))
            new_atlas.paste(atlas)
            atlas = new_atlas

            for img_obj in column_imgs:
                label = img_obj["label"]
                img = img_obj["img"]

                textures_coord.add_data(label, GenerateAtlasCoordTexture(
                    x=offset_x,
                    y=offset_y,
                    width=img.width,
                    height=img.height,
                ))

                atlas.paste(img, (offset_x, offset_y))
                offset_y += img.height

        return atlas, textures_coord

    def __len__(self):
        return len(self.texture_store)

    def __iter__(self) -> Iterator[AtlasTexture]:
        for texture in self.textures:
            yield texture
