from map import Map
from perlin import Perlin, gradient


class Town(Perlin, Map):
    def __init__(self, shape, scale, octave, pers, lac):
        # Inherits from the Perlin and Map classes
        Perlin.__init__(self, shape, scale, octave, pers, lac)
        Map.__init__(self, mode='1', size=shape)

    def generate_map(self, stretch):
        """Generate a black and white map of the town.
        
        Arguments:
            - stretch : float between 0 and 1 (optimal = 0.2)
                (0 = nonexistent, 1 = fully developed)"""
        # Generate a noise map
        self.generate_noise()

        # Get the circular gradient
        grad = gradient(self.shape[0], self.shape[1])
        
        # For each pixel:
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                noise_value = grad[i][j] * (self.noiseMap[i][j] + 1) / 2

                if noise_value < stretch:
                    self.pix[i, j] = 0
                else:
                    self.pix[i, j] = 1
