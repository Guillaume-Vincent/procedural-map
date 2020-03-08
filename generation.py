from world import World


shape = (1000, 1000)
scale = 300.0
octaves = 5
persistence = 0.5
lacunarity = 2.0
waterLevel = -0.2


map = World(shape, scale, octaves, persistence, lacunarity, waterLevel)
map.generateMap()
map.showMap()
map.saveMap(fileName="examples/std.png")
