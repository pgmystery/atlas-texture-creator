class AtlasTexture:
    def __init__(self, id, texture_path: str, label: str):
        self.id = id
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
