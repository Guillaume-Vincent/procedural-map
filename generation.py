from world import World
from random import randint


shape = (1920, 1080)
scale = 700
octaves = 6
persistence = 0.5
lacunarity = 2.0
waterLevel = -0.2


map = World(shape, scale, octaves, persistence, lacunarity, waterLevel)
map.generateMap()

townOctaves = 5
townPersistence = 0.5
townLacunarity = 1.5

for i in range(5):
    size = randint(20, 175)
    townScale = size // 4
    townShape = (size, size)
    townStretch = randint(150, 250) / 1000
    map.addTown(shape=townShape, scale=townScale,
                octaves=townOctaves, persistence=townPersistence,
                lacunarity=townLacunarity, stretch=townStretch)
map.showMap()
map.saveMap(fileName="towns/std.png")