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


"""Validate weighted PTU frames and sparse frame reconstruction."""

import numpy as np

from test_support import prepare_imports, report_close, report_equal

prepare_imports()

from Modes.Extract_from_PTU.include.phconvert_reader import PhconvertPTUreader
from Modes.Phot2conc.Phot2conc_INIT import _Phot2conc_vars_funct


# Synthetic photon coordinates avoid dependence on a physical PTU file.
print("Purpose: verify per-frame weighting and lossless sparse reconstruction.")
print("Synthetic photons cover two frames, two pixels and selected TCSPC bins.")

reader = object.__new__(PhconvertPTUreader)
reader.image_height = 2
reader.image_width = 2
reader.frame_coordinates = {
    "frame": np.array([0, 0, 1, 1, 1]),
    "line": np.array([0, 1, 0, 0, 1]),
    "pixel": np.array([0, 1, 0, 0, 1]),
    "detector": np.array([0, 0, 0, 0, 1]),
    "microtime": np.array([0, 2, 2, 1, 2]),
    "number_of_frames": 2,
    "number_of_tcspc_channels": 3,
}

frames = reader.accumulate_frame_images(0, [0, 2], weights=[1.0, 0.5])
expected_frames = np.array([
    [[1.0, 0.0], [0.0, 0.5]],
    [[0.5, 0.0], [0.0, 0.0]],
])
report_equal("Direct weighted foreground frames", expected_frames, frames, "weighted counts")

sparse = reader.frame_image_data(
    detector=0,
    microtime_bins=[0, 2],
    foreground_weights=[1.0, 0.5],
    background_weights=[0.0, 0.25],
)
mode = object.__new__(_Phot2conc_vars_funct)
mode.pkl_data = {"frame_data_1": sparse}
restored = list(mode._iter_frame_images("1"))

restored_foreground = np.array([item[0] for item in restored])
restored_background = np.array([item[1] for item in restored])
expected_background = np.array([
    [[0.0, 0.0], [0.0, 0.25]],
    [[0.25, 0.0], [0.0, 0.0]],
])

report_equal("Sparse frame offsets", [0, 2, 3], sparse["frame_offsets"])
report_close("Restored foreground frames", expected_frames, restored_foreground, "weighted counts")
report_close("Restored background frames", expected_background, restored_background, "weighted counts")

# Phot2conc must retain fractional TCSPC weights in its integrated image.
fractional_intensity = np.array([
    [0.25, 1.75],
    [2.5, 4.125],
])
calculation_intensity = mode._calculation_intensity(fractional_intensity)
report_equal("Calculation intensity dtype", "float32", str(calculation_intensity.dtype))
report_close(
    "Fractional calculation intensity",
    fractional_intensity,
    calculation_intensity,
    "weighted counts",
)

print("PASS: weighted and sparse frame data")
