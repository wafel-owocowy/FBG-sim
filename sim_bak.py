import numpy as np


class FBG:
    def __init__(self, base_refractive_index, length):
        self.length = length
        self.base_refractive_index = base_refractive_index
        self.dots: list[GratingDot] = []

    def get_refractive_index(self, length_z):
        return self.base_refractive_index + sum([dot.get_refractive_index_offset(length_z) for dot in self.dots])

    def add_dot(self, dot_center: float, dot_size: float, max_refraction: float, rng=None):
        if rng is None:
            self.dots.append(GratingDot(dot_center, dot_size, max_refraction))
        else:
            _dot_center = rng.normal(dot_center, 0.01 * dot_center)
            _dot_size = rng.normal(dot_size, 0.01 * dot_size)
            _max_refraction = rng.normal(max_refraction, 0.01 * max_refraction)
            self.dots.append(GratingDot(_dot_center, _dot_size, _max_refraction))

    def get_transfer_matrix(self, step):
        start_matrix = np.array([[1, 0], [0, 1]],dtype=np.float64)
        print(start_matrix)
        for val in np.linspace(0, stop=self.length, num=int(self.length / step), endpoint=False):
            n = self.get_refractive_index(val)
            n_plus_one = self.get_refractive_index(val + step)
            next_array = np.array([[n + n_plus_one, n - n_plus_one], [n - n_plus_one, n + n_plus_one]],dtype=np.float64)
            if n != 1.44:
                print(np.dot(start_matrix, next_array))
            start_matrix = np.dot(start_matrix, next_array) * (1 / (2 * n))

        return start_matrix


class GratingDot:
    def __init__(self, dot_center: float, dot_size: float, max_refraction: float):
        self.dot_center = dot_center
        self.dot_size = dot_size
        self.max_refraction = max_refraction

    # Testowa funkcja
    def get_refractive_index_offset(self, length_z):
        distance_from_center = self.dot_center - length_z
        if abs(distance_from_center) < self.dot_size:
            return self.max_refraction
        return 0

    def __str__(self):
        return f'center {self.dot_center}, size {self.dot_size}, max refraction {self.max_refraction}'


if __name__ == "__main__":
    rng = np.random.default_rng()
    test_FBG = FBG(1.44, 1.2)
    for i in np.linspace(0.1, 1.1):
        test_FBG.add_dot(i, 0.001, 0.01, rng)
    test_FBG.add_dot(1, 0.001, 0.01)
    test_FBG.add_dot(1.005, 0.001, 0.01, rng)
    print(test_FBG.get_transfer_matrix(0.00001))
