import math


class AtlasCollection:
    def __init__(self):
        self.row_counter = 0
        self.column_counter = 0
        self.collection_length = 0
        self.collection = []
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

    def add_texture(self, texture_path: str, label: str):
        current_offset_number = math.floor(math.sqrt(self.collection_length))
        atlas_texture = AtlasTexture(texture_path, label)

        # 0, 0
        if current_offset_number == 0:
            self.collection.append([atlas_texture])
            self.collection_length += 1
            return

        if self.column_counter == self.row_counter:
            self.column_counter += 1
            self.collection[self.row_counter].append(atlas_texture)
            self.collection_length += 1
        else:
            self.row_counter += 1
            collection_square_len = math.sqrt(self.collection_length)
            if collection_square_len.is_integer():
                pass
            # elif self.column_counter > self.row_counter:
            else:
                column_counter = self.column_counter - 1

    def replace_texture(self):
        pass

    def generate_atlas(self):
        pass


class AtlasTexture:
    def __init__(self, texture_path: str, label: str):
        self.texture_path = texture_path
        self._label = label

    @property
    def texture(self):
        return self.texture_path

    @texture.setter
    def texture(self, path: str):
        self.texture_path = path

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, text: str):
        self._label = text
