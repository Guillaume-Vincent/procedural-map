from PIL import Image


class Map:
    def __init__(self, mode, size):
        self.image = Image.new(mode, size)
        self.pix = self.image.load()

    def show(self):
        self.image.show()

    def save_as(self, file_name):
        self.image.save(file_name)
