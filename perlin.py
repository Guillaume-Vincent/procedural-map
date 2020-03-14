"""Generation parameters:
-scale: number that determines at what distance to view the noise map
-octaves: the number of levels of detail the perlin noise will have
-lacunarity: adjusts frequency(how much detail is added/removed at each octave)
-persistence: how much an octave contributes to the overall shape (amplitude).
"""

from bresenham import bresenham
from random import randint
from noise import pnoise2
from numpy import linspace, sqrt, zeros


def gradient(len_x, len_y):
    """Create a gradient of altitude."""
    x_axis = linspace(-1, 1, len_x)[:, None]
    y_axis = linspace(-1, 1, len_y)[None, :]

    arr = sqrt((x_axis ** 2 + y_axis ** 2) / 2)
    return arr


def list_neighbours(loc_list: list):
    """Return a list of the neighbours of the elements of a given list that are not already in the list."""
    neigh_list = []
    for loc in loc_list:
        neigh_list += [loc_neighbours(loc)[n] for n in range(8) if loc_neighbours(loc)[n] not in loc_list + neigh_list]
    return neigh_list


def loc_neighbours(loc: tuple):
    """Return a list of all the direct neighbours of the given point."""
    neighbours_list = [(loc[0] - 1, loc[1] - 1), (loc[0] - 1, loc[1]), (loc[0] - 1, loc[1] + 1),
                       (loc[0], loc[1] - 1), (loc[0], loc[1] + 1),
                       (loc[0] + 1, loc[1] - 1), (loc[0] + 1, loc[1]), (loc[0] + 1, loc[1] + 1)]
    return neighbours_list


def straight_line(from_loc, to_loc):
    """Return a list containing all the points from a to b in a straight line."""
    return bresenham(from_loc[0], from_loc[1],
                     to_loc[0], to_loc[1])


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

    def generate_noise(self):
        """Generate a noise map."""
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

    def get_delta_h(self):
        """Get the average variation of height in the noise map."""
        delta_list = []
        for i in range(15):
            for j in range(15):
                delta_list.append(abs(self.noiseMap[i][j] - self.noiseMap[i][j + 1]))
                delta_list.append(abs(self.noiseMap[i][j] - self.noiseMap[i + 1][j]))
        return sum(delta_list) / len(delta_list)

    def points_higher_than(self, min_value):
        """Return a list of all the points of the noiseMap higher than minValue."""
        points_list = []
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                if self.noiseMap[i][j] > min_value:
                    points_list.append((i, j))
        return points_list

    def points_lower_than(self, max_value):
        points_list = []
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                if self.noiseMap[i][j] < max_value:
                    points_list.append((i, j))
        return points_list
