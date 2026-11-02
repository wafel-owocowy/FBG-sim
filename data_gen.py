# Program służący do generowania siatek do testowania metod identyfikacji

from time import time
import random
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
import numpy as np
from sim import FBG


def gen_results_csv(outfile: Path, grating: FBG, gen_range: tuple[float, float, float]):
    c = 299792458
    result = ""
    for wavelength in np.arange(gen_range[0], gen_range[1], gen_range[2]):
        reflection_db = grating.get_reflection_db(0.000005, c / (wavelength * 0.000000001))
        result += f"{wavelength:.4f},{reflection_db}\n"
    return (outfile, result)


if __name__ == "__main__":
    # zmienne i stałe
    seed = 256
    base_refractive_index = 1.47
    max_refractive_index = 1.55
    grating_length = 0.1

    result_paths = []
    gratings = []
    ranges = []
    random.seed(seed)
    # losowo perturbowane siatki - 1555 nm
    #
    # for i in range(4):
    #    blocked_wavelength = 1555.004
    #    outfile = Path(f"data/1555-defects/{i:03d}.csv")
    #    if not outfile.exists():
    #        result_paths.append(outfile)
    #        gratings.append(FBG(base_refractive_index, grating_length, blocked_wavelength, max_refractive_index,
    #                            random.randint(0, 2 ** 32 - 1)))
    #        ranges.append((15000,16000))
    #    else:
    #        random.randint(0, 2 ** 32 - 1)

    random.seed(seed)
    for i in range(1):
        blocked_wavelength = random.uniform(1300, 1700)
        outfile = Path(f"data/different-blocked-frequencies/{i:03}.csv")
        if not outfile.exists():
            result_paths.append(outfile)
            gratings.append(FBG(base_refractive_index, grating_length, blocked_wavelength * 0.000000001, max_refractive_index,
                                random.randint(0, 2 ** 32 - 1)))
            ranges.append((blocked_wavelength - 5, blocked_wavelength + 5, 0.01))
    # wielowątkowa generacja wyników dla wcześniej wygenerowanych siatek
    for item in zip(result_paths, gratings, ranges):
        print(*item)
    with ProcessPoolExecutor(max_workers=8) as executor:
        for result in executor.map(gen_results_csv, result_paths, gratings, ranges):
            print(result[0])
            result[0].open("w").write(result[1])
