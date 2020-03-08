"""Generation parameters:
-scale: number that determines at what distance to view the noisemap
-octaves: the number of levels of detail the perlin noise will have
-lacunarity: adjusts frequency(how much detail is added/removed at each octave)
-persistence: how much an octave contributes to the overall shape (amplitude).
"""

from random import randint
from noise import pnoise2
from numpy import zeros


class Perlin():
    def __init__(self, shape, scale, oct, pers, lac):
        # Generation parameters
        self.shape = shape
        self.scale = scale
        self.octaves = oct
        self.persistence = pers
        self.lacunarity = lac

        # Randomness settings
        self.repeatx = randint(shape[0], 50000)
        self.repeaty = randint(shape[1], 50000)
        self.origin = (randint(0, 50000), randint(0, 50000))

        # Noise map
        self.noiseMap = zeros(self.shape)

    def getMap(self):
        """Return a randomly generated noise map."""
        self.__generateNoise()
        return self.noiseMap

    def __generateNoise(self):
        """Generater a noise map"""
        self.__clear()
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                # pnoise2 returns values between -1.0 and 1.0
                noiseValue = pnoise2((self.origin[0]+i)/self.scale,
                                     (self.origin[1]+j)/self.scale,
                                     octaves=self.octaves,
                                     persistence=self.persistence,
                                     lacunarity=self.lacunarity,
                                     repeatx=self.repeatx,
                                     repeaty=self.repeaty)

                # Assign the generated value to an element of the noiseMap
                self.noiseMap[i][j] = noiseValue

    def __clear(self):
        """Clear the noise map"""
        self.noiseMap = zeros(self.shape)
