from map import Map
from perlin import Perlin
from terrain import Terrain
from town import Town

from random import choice, choices, randint
from sys import exit


class World(Perlin, Map):
    def __init__(self, shape, scale, octave, pers, lac, water_level):
        # Inherits from the Perlin and Map classes
        Perlin.__init__(self, shape, scale, octave, pers, lac)
        Map.__init__(self, mode='RGB', size=shape)

        # Level below which the noise value is considered water
        self.waterLevel = water_level

    def generate_map(self):
        # Generate a noise map
        self.generate_noise()

        # For each pixel:
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                # Get the value of a specific noise pixel
                noise_value = self.noiseMap[i][j]

                # Assign a texture to a pixel relative to the noise value
                if noise_value < (self.waterLevel - 0.2):
                    self.pix[i, j] = Terrain.deepWater
                elif noise_value < self.waterLevel:
                    self.pix[i, j] = Terrain.water
                elif noise_value < (self.waterLevel + 0.01):
                    self.pix[i, j] = Terrain.sand
                elif noise_value < (self.waterLevel + 0.05):
                    self.pix[i, j] = Terrain.beach
                elif noise_value < (self.waterLevel + 0.15):
                    self.pix[i, j] = Terrain.plain
                elif noise_value < (self.waterLevel + 0.35):
                    self.pix[i, j] = Terrain.forest
                elif noise_value < (self.waterLevel + 0.42):
                    self.pix[i, j] = Terrain.mountain
                else:
                    self.pix[i, j] = Terrain.snow

    def add_town(self, shape, scale, octaves, persistence, lacunarity, stretch):
        """Randomly place a town of a given (maximum) size on the map"""
        town_loc = self.find_buildable_location(shape[0])
        town_map = Town(shape, scale, octaves, persistence, lacunarity)
        town_map.generate_map(stretch)

        m = 0
        n = 0
        for i in range(town_loc[0] - shape[0] // 2,
                       town_loc[0] + shape[0] // 2 + shape[0] % 2 - 1):
            for j in range(town_loc[1] - shape[1] // 2,
                           town_loc[1] + shape[1] // 2 + shape[1] % 2 - 1):
                if town_map.pix[m, n] == 0:
                    self.pix[i, j] = Terrain.town
                n += 1
            n = 0
            m += 1

    def find_buildable_location(self, town_size):
        """Find a place to build a town on the map and return its location"""
        errmsg = "Could not find a suitable place for a town in this map." \
                 "Try reducing the size of the town and changing the terrain"

        loc = (randint(0 + town_size, self.shape[0] - town_size),
               randint(0 + town_size, self.shape[1] - town_size))
        valid_spot = False
        loop_count = 0
        while valid_spot is False:
            while self.pix[loc[0], loc[1]] not in Terrain.buildableList:
                loc = (randint(0 + town_size, self.shape[0] - town_size),
                       randint(0 + town_size, self.shape[1] - town_size))

            # Presumption of innocence (True while not false)
            valid_spot = True

            # Image center will be at north-west pos if town_size is even
            for i in range(loc[0] - town_size // 2,
                           loc[0] + town_size // 2 + town_size % 2 - 1):
                for j in range(loc[1] - town_size // 2,
                               loc[1] + town_size // 2 + town_size % 2 - 1):
                    if self.pix[i, j] not in Terrain.buildableList:
                        valid_spot = False
                        break  # Break out of second for loop
                if valid_spot is False:
                    break  # Break out of first for loop
            loop_count += 1
            if loop_count > 5000:
                exit(errmsg)

        return loc

    def add_river(self, start_min_height):
        # Choose a starting location at random
        start_list = self.points_higher_than(start_min_height)
        if not start_list:  # if start_list is empty
            exit("No starting location found")

        # Picking a starting location at random
        riv = choice(start_list)

        river_end = False
        still_searching = False
        search_dist = 1
        while river_end is False:
            lower_neighbours = []
            weights = []

            if 0 < riv[0] < self.shape[0] and 0 < riv[1] < self.shape[1]:
                self.pix[riv[0], riv[1]] = Terrain.river
            else:
                break  # river met his end prematurely

            if still_searching is False:
                search_dist = 1

            for neigh in self.neighbours(dist=search_dist, loc=riv):
                if 0 < neigh[0] < self.shape[0] and 0 < neigh[1] < self.shape[1]:
                    if search_dist == 1 and self.pix[neigh[0], neigh[1]] == Terrain.water:
                        river_end = True

                    elif self.noiseMap[neigh[0]][neigh[1]] < self.noiseMap[riv[0]][riv[1]]:
                        lower_neighbours.append(neigh)
                        delta_h = self.noiseMap[riv[0]][riv[1]] - self.noiseMap[neigh[0]][neigh[1]]
                        weights.append(delta_h)

            if not lower_neighbours:  # if lower_neighbours is still empty
                search_dist += 1
                still_searching = True
                if search_dist == 50:
                    river_end = True

            if lower_neighbours and not river_end:
                riv = choices(lower_neighbours, weights)[0]
                still_searching = False




