import csv
import dataclasses
from pathlib import Path
from matplotlib import pyplot as plt


class Readings:
    def __init__(self, filename=None):
        self.wavelengths = []
        self.reflection_level = []
        if filename:
            self.load_from_file(filename)

    def load_from_file(self, filename: Path, trace=1):
        with open(filename) as f:
            x_row = (trace - 1) * 2
            y_row = (trace - 1) * 2 + 1
            reader = csv.reader(f)
            for row in reader:
                if not row[x_row]:
                    break
                self.wavelengths.append(float(row[x_row]))
                self.reflection_level.append(float(row[y_row]))

    def plot_trace(self, out_filename):

        fig, ax = plt.subplots()
        ax.plot(self.wavelengths, self.reflection_level)
        plt.savefig(out_filename)

    def get_readings(self):
        return zip(self.wavelengths, self.reflection_level)


@dataclasses.dataclass
class GratingData:
    wavelength_low: float
    wavelength_high: float
    peak_reflection: float


class FBGPattern:

    def __init__(self, readings,noise_level = -10):
        self.gratings: list[GratingData] = []
        grating_detected = False
        current_grating = None
        for wavelength, reflection_level in readings.get_readings():
            if grating_detected:
                print(wavelength, reflection_level)
                if reflection_level > current_grating.peak_reflection:
                    current_grating.peak_reflection = reflection_level
                if reflection_level < noise_level:
                    grating_detected = False
                    current_grating.wavelength_high = wavelength
                    self.gratings.append(current_grating)
                    current_grating = None
            else:
                if reflection_level > noise_level:
                    grating_detected = True
                    current_grating = GratingData(wavelength_low=wavelength, peak_reflection=reflection_level, wavelength_high=None)

    def is_same_fbg(self, other):
        epsilon = 0.1
        if len(self.gratings) != len(other.gratings):
            return False
        equal_grating_found = 0
        for grating in self.gratings:
            for grating2 in other.gratings:
                if abs(grating.wavelength_low - grating2.wavelength_low) < epsilon and abs(
                        grating.wavelength_high - grating2.wavelength_high) < epsilon:
                    equal_grating_found += 1
                    break
        return equal_grating_found == len(self.gratings)


if __name__ == "__main__":
    readings = Readings()
    readings.load_from_file(Path("fbg1555nm_raw.csv"),trace=2)
    pattern = FBGPattern(readings,noise_level=-70)
    print(pattern.gratings)
