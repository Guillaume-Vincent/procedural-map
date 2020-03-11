"""Generation parameters:
-scale: number that determines at what distance to view the noise map
-octaves: the number of levels of detail the perlin noise will have
-lacunarity: adjusts frequency(how much detail is added/removed at each octave)
-persistence: how much an octave contributes to the overall shape (amplitude).
"""

from random import randint
from noise import pnoise2
from numpy import zeros


class Perlin:
    def __init__(self, shape, scale, octaves, persistence, lacunarity):
        # Generation parameters
        self.shape = shape
        self.scale = scale
        self.octaves = octaves
        self.persistence = persistence
        self.lacunarity = lacunarity

        # Randomness settings
        self.repeatX = randint(shape[0], 50000)
        self.repeatY = randint(shape[1], 50000)
        self.origin = (randint(0, 50000), randint(0, 50000))

        # Noise map
        self.noiseMap = zeros(self.shape)

    def get_map(self):
        """Return a randomly generated noise map."""
        self.generate_noise()
        return self.noiseMap

    def generate_noise(self):
        """Generate a noise map"""
        self.__clear()
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                # The noise function returns values between -1.0 and 1.0
                noise_value = pnoise2((self.origin[0]+i)/self.scale,
                                      (self.origin[1]+j)/self.scale,
                                      octaves=self.octaves,
                                      persistence=self.persistence,
                                      lacunarity=self.lacunarity,
                                      repeatx=self.repeatX,
                                      repeaty=self.repeatY)

                # Assign the generated value to an element of the noiseMap
                self.noiseMap[i][j] = noise_value

    def __clear(self):
        """Clear the noise map"""
        self.noiseMap = zeros(self.shape)

    def points_higher_than(self, min_value):
        """Return a list of all the points of the noiseMap higher than minValue"""
        points_list = []
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                if self.noiseMap[i][j] > min_value:
                    points_list.append((i, j))
        return points_list

    @staticmethod
    def neighbours(loc, dist=1):
        """Return a list of all the points a certain distance away from loc"""
        neighbours_list = []
        for i in range(loc[0] - dist, loc[0] + dist + 1):
            neighbours_list.append((i, loc[1] - dist))
            neighbours_list.append((i, loc[1] + dist))
        for j in range(loc[1] - dist + 1, loc[1] + dist):
            neighbours_list.append((loc[0] - dist, j))
            neighbours_list.append((loc[0] + dist, j))
        return neighbours_list
