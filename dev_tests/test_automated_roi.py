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


import numpy as np

from smICA.Required.automated_roi import ImageROIProcessor


def make_processor_without_detected_objects():
    processor = ImageROIProcessor()
    processor.image = np.array([[10, 20], [30, 40]], dtype=np.uint8)
    processor.all_cells_masks = [
        np.array([[255, 255], [0, 0]], dtype=np.uint8)
    ]
    processor._process_contours_pipeline = lambda image, threshold: ([], [])
    return processor


def test_subtract_mode_keeps_cell_roi_when_no_object_is_detected():
    processor = make_processor_without_detected_objects()

    processor.detect_objects_inside(
        threshold=1.036,
        mode="dark",
        subtract=True,
    )

    np.testing.assert_array_equal(
        processor.all_masks[0],
        processor.all_cells_masks[0],
    )


def test_find_mode_returns_empty_roi_when_no_object_is_detected():
    processor = make_processor_without_detected_objects()

    processor.detect_objects_inside(
        threshold=1.036,
        mode="dark",
        subtract=False,
    )

    np.testing.assert_array_equal(
        processor.all_masks[0],
        np.zeros_like(processor.all_cells_masks[0]),
    )
