# This file is part of the smICA repository that is distributed under the MIT license; see below.
#
#
# ############################################################################
#
# MIT License
#
# Copyright (c) 2026 Tomasz Kalwarczyk
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


"""Validate the main Phot2conc numerical conversions."""

from math import sqrt

import numpy as np

from test_support import prepare_imports, report_close

prepare_imports()

from Modes.Phot2conc.Phot2conc_INIT import _Phot2conc_vars_funct


# Fixed reference values make accidental formula changes visible.
print("Purpose: validate calibration and photon-to-concentration formulas.")
print("Inputs: omega=0.2 um, kappa=5.1, dwell=10 us, 2 frames.")
print("Brightness=2e4 Hz/molecule; uncertainties: 0.01 um, 0.2 and 1e3 Hz/molecule.")

volume, volume_error = _Phot2conc_vars_funct.VEFF(None, 0.2, 5.1, 0.01, 0.2)
report_close("Effective focal volume", 0.22718778227073372, volume, "um^3")
report_close("Effective-volume uncertainty", 0.03522353698304855, volume_error, "um^3")

molecules, molecules_error = _Phot2conc_vars_funct.calc_molecules(
    None, np.array([4.0, 8.0]), 10.0, 2, 20_000.0, 1_000.0
)
report_close("Molecules per pixel", [10.0, 20.0], molecules, "molecules/pixel")
report_close("Molecule-number uncertainty", [0.5, 1.0], molecules_error, "molecules/pixel")

concentration, concentration_error = _Phot2conc_vars_funct.CONC(
    None,
    molecules[0],
    volume * 1e-15,
    molecules_error[0],
    volume_error * 1e-15,
)
report_close("Concentration", 73.09103731621561, concentration * 1e9, "nM")
report_close("Concentration uncertainty", 11.906857526692937, concentration_error * 1e9, "nM")

mean, sem = _Phot2conc_vars_funct._mean_and_sem([1.0, 2.0, 3.0, float("nan")])
report_close("Finite-pixel mean and SEM", [2.0, 1.0 / sqrt(3.0)], [mean, sem], "counts")

# Two adjacent pixels separated by 0.1 um share a Gaussian observation area
# with omega=0.2 um. Their effective sample size is 2 / (1 + exp(-0.25)).
adjacent_pixels = np.ones((1, 2), dtype=float)
effective_pixels = _Phot2conc_vars_funct._effective_pixel_count(
    adjacent_pixels,
    pixel_size_nm=100.0,
    omega_um=0.2,
)
expected_effective_pixels = 2.0 / (1.0 + np.exp(-0.25))
report_close(
    "Effective pixel count for overlapping observations",
    expected_effective_pixels,
    effective_pixels,
    "independent pixels",
)

# The default error combines effective SEM and the shared calibration error.
concentration_values = np.array([1.0, 3.0])
calibration_errors = np.array([0.5, 1.5])
sem_only_error = _Phot2conc_vars_funct._reported_mean_error(
    concentration_values,
    calibration_errors,
    effective_count=2.0,
    sem_only=True,
)
combined_error = _Phot2conc_vars_funct._reported_mean_error(
    concentration_values,
    calibration_errors,
    effective_count=2.0,
    sem_only=False,
)
report_close("Effective SEM-only error", 1.0, sem_only_error, "nM")
report_close("Combined SEM and calibration error", sqrt(2.0), combined_error, "nM")

print("PASS: Phot2conc numerical conversions")
