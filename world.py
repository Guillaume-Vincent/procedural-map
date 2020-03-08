from perlin import Perlin
from terrain import Terrain
from PIL import Image
from random import randint
from math import sqrt
from town import Town


def distance(a, b):
    """Return the distance between two 2D points a and b"""
    return sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)


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
        self.pix = self.worldMap.load()

        # For each pixel:
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                # Get the noiseValue given during noise map generation
                noiseValue = self.noiseMap[i][j]

                # Assign a texture to a pixel relative to the noiseValue
                if noiseValue < (self.waterLevel - 0.2):
                    self.pix[i, j] = Terrain.deepwater
                elif noiseValue < (self.waterLevel):
                    self.pix[i, j] = Terrain.water
                elif noiseValue < (self.waterLevel + 0.01):
                    self.pix[i, j] = Terrain.sand
                elif noiseValue < (self.waterLevel + 0.05):
                    self.pix[i, j] = Terrain.beach
                elif noiseValue < (self.waterLevel + 0.15):
                    self.pix[i, j] = Terrain.plain
                elif noiseValue < (self.waterLevel + 0.35):
                    self.pix[i, j] = Terrain.forest
                elif noiseValue < (self.waterLevel + 0.42):
                    self.pix[i, j] = Terrain.mountain
                else:
                    self.pix[i, j] = Terrain.snow

    def addTown(self, shape, scale, octaves, persistence, lacunarity, stretch):
        """Randomly place a town of a given (maximum) size on the map"""
        townLoc = self.findBuildableLocation(shape[0])
        townMap = Town(shape, scale, octaves, persistence, lacunarity)
        townMap.generateMap(stretch)

        m = 0
        n = 0
        for i in range(townLoc[0] - shape[0] // 2,
                       townLoc[0] + shape[0] // 2 + shape[0] % 2 - 1):
            for j in range(townLoc[1] - shape[1] // 2,
                           townLoc[1] + shape[1] // 2 + shape[1] % 2 - 1):
                if townMap.pix[m, n] == 0:
                    self.pix[i, j] = Terrain.town
                n += 1
            n = 0
            m += 1

    def showMap(self):
        """Dislay the map"""
        self.worldMap.show()

    def saveMap(self, fileName):
        """Save the map in the given file"""
        self.worldMap.save(fileName)

    def drawSquare(self, location, size=5, color=Terrain.pink):
        """Draw a plain square on the map at the given location"""
        for i in range(location[0] - size, location[0] + size):
            for j in range(location[1] - size, location[1] + size):
                self.pix[i, j] = color

    def findBuildableLocation(self, townSize):
        """Find a place to build a town on the map and return its location"""
        validSpot = False
        errmsg1 = "Could not find a suitable place for a town in this map\n"
        errmsg2 = "Try reducing the size of the town and changing the terrain"

        loopCount = 0
        while validSpot is False:
            loc = (randint(0 + townSize, self.shape[0] - townSize),
                   randint(0 + townSize, self.shape[1] - townSize))
            while self.pix[loc[0], loc[1]] not in Terrain.buildableList:
                loc = (randint(0 + townSize, self.shape[0] - townSize),
                       randint(0 + townSize, self.shape[1] - townSize))

            # Presumption of innocence (True while not false)
            validSpot = True

            # Image center will be at north-west pos if townSize is even
            for i in range(loc[0] - townSize // 2,
                           loc[0] + townSize // 2 + townSize % 2 - 1):
                for j in range(loc[1] - townSize // 2,
                               loc[1] + townSize // 2 + townSize % 2 - 1):
                    if self.pix[i, j] not in Terrain.buildableList:
                        validSpot = False
                        break  # Break out of second for loop
                if validSpot is False:
                    break  # Break out of first for loop
            loopCount += 1
            if loopCount > 5000:
                return(errmsg1+errmsg2)

        self.drawSquare(location=loc)
        return loc
