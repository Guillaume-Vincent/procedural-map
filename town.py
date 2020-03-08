from perlin import Perlin
from PIL import Image
import numpy as np


def gradient(xlen, ylen):
    x_axis = np.linspace(-1, 1, xlen)[:, None]
    y_axis = np.linspace(-1, 1, ylen)[None, :]

    arr = np.sqrt((x_axis ** 2 + y_axis ** 2) / 2)
    return arr

class Town(Perlin):
    def __init__(self, shape, scale, oct, pers, lac):
        # Inherits from the Perlin class
        Perlin.__init__(self, shape, scale, oct, pers, lac)

        # Creation of a black and white image object
        self.townMap = Image.new(mode='1', size=self.shape)

    def generateMap(self, stretch):
        """Generate a black and white map of the town.
        
        Arguments:
            - stretch : float between 0 and 1 (optimal = 0.2)
                (0 = inexisting, 1 = fully developped)"""
        # Generate a noise map
        self._Perlin__generateNoise()

        # Load the pixels of the image
        self.pix = self.townMap.load()

        # Get the circular gradient
        grad = gradient(self.shape[0], self.shape[1])
        
        # For each pixel:
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                noiseValue = grad[i][j] * (self.noiseMap[i][j] + 1) / 2

                if noiseValue < stretch:
                    self.pix[i, j] = 0
                else:
                    self.pix[i, j] = 1

    def showMap(self):
        """Dislay the map"""
        self.townMap.show()

    def saveMap(self, fileName):
        """Save the map in the given file"""
        self.townMap.save(fileName)
