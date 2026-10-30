import csv
from pathlib import Path
from matplotlib import pyplot as plt


class Readings:
    def __init__(self,):
        self.wavelengths = []
        self.reflection_level = []

    def load_from_file(self, filename:Path,trace = 1):
        with open(filename) as f:
            x_row = (trace - 1) * 2
            y_row = (trace - 1) * 2 + 1
            print(x_row, y_row)
            reader = csv.reader(f)
            for row in reader:
                if not row[x_row]:
                    break
                self.wavelengths.append(float(row[x_row]))
                self.reflection_level.append(float(row[y_row]))

    def plot_trace(self, out_filename, noise_level):

        fig, ax = plt.subplots()
        ax.plot(self.wavelengths, self.reflection_level)
        plt.savefig(out_filename)