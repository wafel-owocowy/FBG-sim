import math
import cmath
import matplotlib.pyplot as plt
import numpy as np
import vnoise


class FBG:
    def __init__(self, base_refractive_index, length, blocked_wavelength, max_refractive_index, seed=None):
        self.max_refractive_index = max_refractive_index
        self.blocked_wavelength = blocked_wavelength
        self.length = length
        self.base_refractive_index = base_refractive_index
        self.transfer_matrix = None
        self.grating_period = blocked_wavelength / (2 * math.pi)
        if seed is not None:
            self.noise_fun = vnoise.Noise(seed)
        else:
            self.noise_fun = None

    def get_refractive_index(self, length_z):
        if self.noise_fun is not None:
            noise = self.noise_fun.noise1(length_z * 1000000, octaves=4, persistence=0.7) * 1 * (
                    self.max_refractive_index - self.base_refractive_index)
        else:
            noise = 0
        refractive_index = self.base_refractive_index + math.sin(length_z / self.grating_period) * (
                self.max_refractive_index - self.base_refractive_index) + noise
        return refractive_index

    def get_transfer_matrix(self, step, frequency):
        transfer_matrix = np.array([[1, 0], [0, 1]], dtype=np.complex64)
        c = 299792458
        m_matrix = np.array([[cmath.exp(1j * 2 * math.pi * frequency / c * step), 0],
                             [0, cmath.exp(-1j * 2 * math.pi * frequency / c * step)]], dtype=np.complex64)
        for val in np.linspace(0, stop=self.length, num=int(self.length / step), endpoint=False):
            n = self.get_refractive_index(val)
            n_plus_one = self.get_refractive_index(val + step)
            i_matrix = np.array([[n + n_plus_one, n - n_plus_one], [n - n_plus_one, n + n_plus_one]],
                                dtype=np.complex64) * (1 / (2 * n))
            transfer_matrix @= i_matrix
            transfer_matrix @= m_matrix

        return transfer_matrix

    def get_reflection_db(self, step, frequency):
        transfer_matrix = self.get_transfer_matrix(step, frequency)
        return np.log10(np.abs(transfer_matrix[1, 0] / transfer_matrix[0, 0])) * 10
        pass

    def __str__(self):
        return f"base_refractive_index={self.base_refractive_index}, length={self.length}, blocked_wavelength={self.blocked_wavelength}, max_refractive_index={self.max_refractive_index}"


if __name__ == "__main__":
    # zmienne i stałe
    c = 299792458
    base_refractive_index = 1.47
    max_refractive_index = 1.55
    grating_length = 0.1
    blocked_wavelength = 1555.004 * 0.000000001

    # Zaszumienie siatki (przesadzone dla efektu) - linowy perlin noise
    perturbed_FBG = FBG(base_refractive_index, grating_length, blocked_wavelength, max_refractive_index, 1225)
    print(perturbed_FBG)
    clean_FBG = FBG(base_refractive_index, grating_length, blocked_wavelength, max_refractive_index)
    points_x = np.linspace(0, 0.00001, num=200)
    points_perturbed = []
    points_clean = []
    for i in points_x:
        points_perturbed.append(perturbed_FBG.get_refractive_index(i))
        points_clean.append(clean_FBG.get_refractive_index(i))
    fig, ax = plt.subplots()
    ax.plot(points_x, points_perturbed, label="Siatka zaszumiona")
    ax.plot(points_x, points_clean, label="Siatka czysta")
    ax.plot(points_x, [base_refractive_index] * len(points_x), label="Refrakcja światłowodu")
    fig.legend()
    plt.savefig("perturbacje_siatki.png")

    # Macierz przejścia
    transfer_matrix = clean_FBG.get_transfer_matrix(0.000001, 5000000000)
    print(transfer_matrix)
    print(transfer_matrix[1, 0] / transfer_matrix[0, 0])
    print(clean_FBG.get_reflection_db(0.000001, 5000000000))
    print(np.abs(transfer_matrix[1, 0] / transfer_matrix[0, 0]))
    transfer_matrix = clean_FBG.get_transfer_matrix(0.000001, c / blocked_wavelength)
    print(transfer_matrix)
    print(transfer_matrix[1, 0] / transfer_matrix[0, 0])
    print(clean_FBG.get_reflection_db(0.000001, c / blocked_wavelength))
    # -47.940 dB bez -75.219 dB z
