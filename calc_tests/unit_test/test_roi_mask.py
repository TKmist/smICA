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


"""Validate conversion of detected contours into ROI masks."""

import cv2
import numpy as np

from test_support import prepare_imports, report_equal

prepare_imports()

from Required.automated_roi import ImageROIProcessor


# A contour from (1, 1) to (3, 3) covers exactly nine image pixels.
print("Purpose: verify conversion of a geometric contour into a binary ROI mask.")
print("The 2 x 2 contour area covers a 3 x 3 set of raster pixels, including edges.")

contour = np.array([[[1, 1]], [[3, 1]], [[3, 3]], [[1, 3]]], dtype=np.int32)
mask = ImageROIProcessor._create_mask([contour], (5, 5))[0]

report_equal("Mask data type", "uint8", str(mask.dtype))
report_equal("Non-zero ROI pixels", 9, np.count_nonzero(mask), "pixels")
report_equal("Geometric contour area", 4.0, cv2.contourArea(contour), "pixel^2")
report_equal("Binary mask levels", [0, 255], np.unique(mask), "intensity")

print("PASS: ROI contour mask")
