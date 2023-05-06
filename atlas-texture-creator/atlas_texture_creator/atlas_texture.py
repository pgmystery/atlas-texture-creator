class AtlasTexture:
    def __init__(self, id: int, texture_path: str, label: str):
        self.row = -1
        self.column = -1
        self.id = id
        self.texture_path = texture_path
        self._label = label

    def get_coord(self):
        return (self.column, self.row)

    def set_coord(self, column: int, row: int):
        self.column = column
        self.row = row

    @property
    def img_path(self):
        return self.texture_path

    @img_path.setter
    def img_path(self, path: str):
        self.texture_path = path

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, text: str):
        self._label = text
