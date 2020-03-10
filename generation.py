from world import World


shape = (3840, 2160)
scale = 700
octaves = 6
persistence = 0.5
lacunarity = 2.0
waterLevel = -0.2

worldMap = World(shape, scale, octaves, persistence, lacunarity, waterLevel)
worldMap.generate_map()

worldMap.show()
