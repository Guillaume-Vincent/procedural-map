from perlin import Perlin
from terrain import Terrain
from PIL import Image


class World(Perlin):
    def __init__(self, shape, scale, oct, pers, lac, waterLevel):
        # Inherits from the Perlin class
        Perlin.__init__(self, shape, scale, oct, pers, lac)

        # Level below which the noise value is considered water (offset)
        self.waterLevel = waterLevel

        # Creation of an (RGB) image object
        self.worldMap = Image.new(mode='RGB', size=self.shape)

    def generateMap(self):
        # Generate a noise map
        self._Perlin__generateNoise()

        # Load the pixels of the image
        pix = self.worldMap.load()

        # For each pixel:
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                # Get the noiseValue given during noise map generation
                noiseValue = self.noiseMap[i][j]

                # Assign a texture to a pixel relative to the noiseValue
                if noiseValue < (self.waterLevel - 0.2):
                    pix[i, j] = Terrain.deepwater
                elif noiseValue < (self.waterLevel):
                    pix[i, j] = Terrain.water
                elif noiseValue < (self.waterLevel + 0.01):
                    pix[i, j] = Terrain.sand
                elif noiseValue < (self.waterLevel + 0.05):
                    pix[i, j] = Terrain.beach
                elif noiseValue < (self.waterLevel + 0.15):
                    pix[i, j] = Terrain.plain
                elif noiseValue < (self.waterLevel + 0.35):
                    pix[i, j] = Terrain.forest
                elif noiseValue < (self.waterLevel + 0.5):
                    pix[i, j] = Terrain.mountain
                else:
                    pix[i, j] = Terrain.snow

    def showMap(self):
        """Dislay the map"""
        self.worldMap.show()

    def saveMap(self, fileName):
        """Save the map in the given file"""
        self.worldMap.save(fileName)
