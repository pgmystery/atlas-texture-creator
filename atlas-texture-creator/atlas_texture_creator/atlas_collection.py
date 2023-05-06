import math
from PIL import Image

from .atlas_texture import AtlasTexture


class AtlasCollection:
    def __init__(self, name: str):
        super().__init__()
        self.name = name
        self.texture_size = 16
        self.texture_id = 1
        self._add_to_column = 0
        self.row_coords = AtlasCoord()
        self.column_coords = AtlasCoord()
        self.collection_length = 0
        self.collection: list[list[AtlasTexture]] = []
        # 1 = self.collection[0][0] = [[1]]  # new array
        # 2 = self.collection[0][1] = [[1, 2]]
        # 3 = self.collection[1][0] = [[1, 2], [3]]  # new array
        # 4 = self.collection[1][1] = [[1, 2], [3, 4]]
        # 5 = self.collection[0][2] = [[1, 2, 5], [3, 4]]
        # 6 = self.collection[2][0] = [[1, 2, 5], [3, 4], [6]]  # new array
        # 7 = self.collection[1][2] = [[1, 2, 5], [3, 4, 7], [6]]
        # 8 = self.collection[2][1] = [[1, 2, 5], [3, 4, 7], [6, 8]]
        # 9 = self.collection[2][2] = [[1, 2, 5], [3, 4, 7], [6, 8, 9]]
        # 10 = self.collection[0][3] = [[1, 2, 5, 10], [3, 4, 7], [6, 8, 9]]
        # 11 = self.collection[3][0] = [[1, 2, 5, 10], [3, 4, 7], [6, 8, 9], [11]]  # new array
        # 12 = self.collection[1][3] = [[1, 2, 5, 10], [3, 4, 7, 12], [6, 8, 9], [11]]
        # 13 = self.collection[3][1] = [[1, 2, 5, 10], [3, 4, 7, 12], [6, 8, 9], [11, 13]]
        # 14 = self.collection[2][3] = [[1, 2, 5, 10], [3, 4, 7, 12], [6, 8, 9, 14], [11, 13]]
        # 15 = self.collection[3][2] = [[1, 2, 5, 10], [3, 4, 7, 12], [6, 8, 9, 14], [11, 13, 15]]
        # 16 = self.collection[3][3] = [[1, 2, 5, 10], [3, 4, 7, 12], [6, 8, 9, 14], [11, 13, 15, 16]]
        # 17 = self.collection[0][4] = [[1, 2, 5, 10, 17], [3, 4, 7, 12], [6, 8, 9, 14], [11, 13, 15, 16]]
        # 18 = self.collection[4][0] = [[1, 2, 5, 10, 17], [3, 4, 7, 12], [6, 8, 9, 14], [11, 13, 15, 16], [18]]  # new array
        # self.collection[self.row_counter][self.column_counter]
        # arrays = row; numbers in array = column
        # column = 0 = new array

    def add_texture(self, texture_path: str, label: str) -> AtlasTexture:
        atlas_texture = AtlasTexture(self.texture_id, texture_path, label)
        self._add_texture(atlas_texture)
        return atlas_texture

    def load_texture(self, texture: AtlasTexture):
        self._add_texture(texture)
        # self.collection[texture.row][texture.column] = texture

    def load_textures(self, textures: list[AtlasTexture]):
        for texture in textures:
            self.load_texture(texture)

    def get_texture(self, row: int, column: int) -> AtlasTexture:
        return self.collection[row][column]

    # Not very efficient...
    def textures(self):
        square_number = math.ceil(math.sqrt(self.collection_length))

        # current_row = 0
        # current_column = 0
        # textures_length_sqrt = math.sqrt(self.collection_length)
        # textures_length_floor_sqrt = math.floor(textures_length_sqrt)
        # max_row = textures_length_floor_sqrt
        # max_column = textures_length_floor_sqrt
        # offset_number = (self.collection_length - (max_row * max_column)) / 2.0
        # row_offset = math.floor(offset_number)
        # column_offset = math.floor(offset_number) if offset_number.is_integer() else math.ceil(offset_number)

        for column in range(square_number):
            for row in range(square_number):
                try:
                    yield self.collection[column][row]
                except IndexError:
                    continue

    def replace_texture(self, new_texture: AtlasTexture):
        column = new_texture.column
        row = new_texture.row
        self.collection[column][row] = new_texture

    def generate_atlas(self) -> Image:
        atlas_size = math.ceil(math.sqrt(self.collection_length)) * self.texture_size
        atlas = Image.new(mode="RGBA", size=(atlas_size, atlas_size))

        for texture in self.textures():
            column = texture.column
            row = texture.row
            x = column * self.texture_size
            y = row * self.texture_size

            img = Image.open(texture.img_path)
            atlas.paste(img, (x, y))

        return atlas

    def _add_texture(self, atlas_texture: AtlasTexture):
        atlas_length = math.sqrt(self.collection_length + 1)
        current_offset = math.floor(atlas_length)
        self.texture_id += 1

        # 0, 0
        if self.collection_length == 0:
            atlas_texture.set_coord(0, 0)
            self.collection.append([atlas_texture])
            self.collection_length += 1
            print(atlas_texture.get_coord())
            return

        if atlas_length.is_integer():
            self.row_coords.next()
            self.column_coords.next()
            atlas_length_index = int(atlas_length) - 1
            atlas_texture.set_coord(atlas_length_index, len(self.collection[atlas_length_index]))
            self.collection[atlas_length_index].append(atlas_texture)
            self._reset_add_to_column()
            self.collection_length += 1
            print(atlas_texture.get_coord())
            return

        if self._add_to_column == 0:
            # add to column
            atlas_texture.set_coord(self.column_coords.offset, len(self.collection[self.column_coords.offset]))
            self.collection[self.column_coords.offset].append(atlas_texture)
            self.column_coords.step()
        else:
            if self.row_coords.offset == 0:
                # add array
                atlas_texture.set_coord(len(self.collection), 0)
                self.collection.append([atlas_texture])
            else:
                atlas_texture.set_coord(current_offset, len(self.collection[current_offset]))
                self.collection[current_offset].append(atlas_texture)
            self.row_coords.step()
        self.collection_length += 1
        self._coord_flip()
        print(atlas_texture.get_coord())

    def _coord_flip(self):
        self._add_to_column = 0 if self._add_to_column == 1 else 1

    def _reset_add_to_column(self):
        self._add_to_column = 0


class AtlasCoord:
    def __init__(self):
        self.index = 0
        self.offset = 0

    def reset(self):
        self.offset = 0

    def step(self):
        self.offset += 1

    def next(self):
        self.index += 1
        self.reset()
