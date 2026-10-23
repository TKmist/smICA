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


from __future__ import annotations

from types import SimpleNamespace

import numpy as np
import pandas as pd

from Modes.Phot2conc import Phot2conc_INIT as phot_module


class FakeDpg:
    def __init__(self):
        self.values = {
            "Auto_ROI_checkbox": False,
            "FILE_ROI_checkbox": False,
            "Error_type_checkbox": False,
            "Brightness_input_ch_1": 10.0,
            "Brightness_err_input_ch_1": 1.0,
            "focal_vol_input_ch_1": 1.0,
            "focal_vol_err_input_ch_1": 0.1,
        }

    def get_value(self, tag):
        return self.values.get(tag)


def make_mode(monkeypatch):
    monkeypatch.setattr(phot_module, "dpg", FakeDpg())
    mode = object.__new__(phot_module._Phot2conc_vars_funct)
    mode.anal_file = "measurement"
    mode.PTU_Px_dwell = 1.0
    mode.processor_1 = SimpleNamespace(all_masks=None, roi_image=None)
    mode.processor_2 = SimpleNamespace(all_masks=None, roi_image=None)
    mode.pkl_data = {
        "frame_intensity_1": np.array([
            [[1.0, 2.0], [3.0, 4.0]],
            [[2.0, 4.0], [6.0, 8.0]],
        ]),
        "frame_bgrnd_1": np.array([
            [[0.0, 0.0], [0.0, 1.0]],
            [[0.0, 1.0], [1.0, 2.0]],
        ]),
    }
    mode.frame_results_by_channel = {}
    mode.frame_results_file = None
    return mode


def test_frame_results_include_foreground_background_and_calibration(monkeypatch):
    mode = make_mode(monkeypatch)

    mode._calculate_frame_results()

    frame_1, frame_2 = mode.frame_results_by_channel["1"]
    assert frame_1["<Counts>"] == 2.5
    assert frame_2["<Counts>"] == 5.0
    assert frame_1["<Background counts>"] == 0.25
    assert frame_2["<Background counts>"] == 1.0
    assert frame_2["<N_p>"] == 2 * frame_1["<N_p>"]
    assert frame_2["<C>"] == 2 * frame_1["<C>"]


def test_frame_results_are_added_only_as_export_columns(monkeypatch):
    mode = make_mode(monkeypatch)
    base_row = pd.DataFrame(
        [["measurement", "ROI_0", 1] + [0.0] * 10],
        columns=mode._base_result_columns(),
    )

    exported = mode._attach_frame_results(base_row)

    assert list(base_row.columns) == mode._base_result_columns()
    assert exported.at[0, "Frame_1_<Counts>"] == 2.5
    assert exported.at[0, "Frame_2_<Counts>"] == 5.0
    assert exported.at[0, "Frame_1_<Background counts>"] == 0.25
    assert exported.at[0, "Frame_2_<Background counts>"] == 1.0


def test_sparse_frame_data_matches_dense_frame_results(monkeypatch):
    mode = make_mode(monkeypatch)
    mode._calculate_frame_results()
    dense_results = mode.frame_results_by_channel["1"]
    mode.pkl_data = {
        "frame_data_1": {
            "format": "sparse_frame_images_v1",
            "shape": (2, 2, 2),
            "frame_offsets": np.array([0, 4, 8]),
            "line": np.array([0, 0, 1, 1, 0, 0, 1, 1]),
            "pixel": np.array([0, 1, 0, 1, 0, 1, 0, 1]),
            "foreground": np.array([1, 2, 3, 4, 2, 4, 6, 8]),
            "background": np.array([0, 0, 0, 1, 0, 1, 1, 2]),
        }
    }

    mode._calculate_frame_results()

    assert mode.frame_results_by_channel["1"] == dense_results


def test_calculation_intensity_preserves_fractional_photon_weights():
    source = np.array([[0.25, 1.75], [12.5, 65536.5]], dtype=np.float64)

    intensity = phot_module._Phot2conc_vars_funct._calculation_intensity(source)

    assert intensity.dtype == np.float32
    np.testing.assert_allclose(intensity, source, rtol=1e-7, atol=0.0)
