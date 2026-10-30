# Program służący do generowania siatek do testowania metod identyfikacji

import random
from pathlib import Path

import numpy as np
from sim import FBG
name = "test"
if __name__ == "__main__":
    # zmienne i stałe
    c = 299792458
    base_refractive_index = 1.47
    max_refractive_index = 1.55
    grating_length = 0.1
    blocked_wavelength = 1555.004 * 0.000000001

    # losowo perturbowane siatki - 1555 nm
    random.seed(256)
    for i in range(1):
        outfile = Path(f"data/1555-defects/{name}_{i:03d}.csv")
        if not outfile.exists():
            with outfile.open("w") as f:
                grating = FBG(base_refractive_index, grating_length, blocked_wavelength,max_refractive_index ,random.randint(0,2^31-1))
                for wavelength in range(15000,16001):
                    wavelength *= 0.1
                    reflection_db = grating.get_reflection_db(0.000001, c / (wavelength * 0.000000001 ))
                    f.write(f"{wavelength:.4f},{reflection_db}\n")