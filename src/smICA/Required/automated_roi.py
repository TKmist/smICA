'''
This file is part of the smICA repository that is distributed under the MIT license; see below.


############################################################################

MIT License

Copyright (c) 2024 Antoni Lis & Tomasz Kalwarczyk

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import os
import cv2
import numpy as np
from collections import defaultdict
from skimage.filters import threshold_multiotsu


class ImageROIProcessor:
    def __init__(self):
        """
        Klasa do przetwarzania obrazów w celu znalezienia ROI (Region of Interest).
        """
        # self.input_path = input_path
        # self.output_path = output_path
        # self.find_nucleus = find_nucleus
        self.image = None
        self.roi_image = None
        self.all_cells_contours = None
        self.all_cells_masks = None

        self.all_masks = None
        self.all_contours = None

        self.all_hierarchy = None

    def load_image(self):
        """
        Wczytuje obraz z podanej ścieżki.
        """
        # self.image = cv2.imread(self.input_path, cv2.IMREAD_GRAYSCALE)

        loaded_image = np.load(self.input_path)

        self.image = (loaded_image * (255 / loaded_image.max())).astype(np.uint8)

        if self.image is None:
            raise FileNotFoundError(f"Nie udało się wczytać obrazu: {self.input_path}")

    def _prepare_roi_image(self):
        """Helper to prepare ROI mask and base image"""
        roi_mask = (self.all_cells_masks[0] / np.max(self.all_cells_masks[0])).astype(np.uint8)
        image = np.clip(self.image, 0, 255).astype(np.uint8)
        return roi_mask, image

    def detect_cell_roi(self, image_to_process, ratio):
        """Finds ROI in image and stores result in roi_image attribute"""
        thresholded = self.preprocess_image(image_to_process, ratio, 'gaussian', 'otsu')
        found_contours, hierarchy = cv2.findContours(thresholded, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        classified = self._classify_contours_by_area(found_contours, hierarchy)

        self.all_cells_masks = self._create_mask(
            [ext_contour for (ext_contour, _) in classified],
            image_to_process.shape
        )
        self.all_cells_contours = [ext_contour for (ext_contour, _) in classified]

    def detect_objects_inside(self, threshold, subtract=False, mode='bright', many=False):
        """Generic function to detect bright or dark spots, single or many."""
        roi_mask, image = self._prepare_roi_image()

        # Invert image for dark mode
        if mode == 'dark':
            image_to_process = (~image * roi_mask).astype(np.uint8)
        else:
            image_to_process = (image * roi_mask).astype(np.uint8)

        if many:
            _, thresh = cv2.threshold(image_to_process, threshold * 10, 255, cv2.THRESH_BINARY)
            num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(thresh)
            print(f"Components found: {num_labels}\nStats:\n{stats}")
            mask = np.where(labels > 0, 255, 0).astype(np.uint8)
        else:
            inside_mask, _ = self._process_contours_pipeline(image_to_process, threshold)
            mask = inside_mask[0]

        if subtract:
            self.all_masks = [self.all_cells_masks[0] - mask]
        else:
            self.all_masks = [mask]

    def _process_contours_pipeline(self, image_to_process, ratio):
        """Unified contour processing pipeline"""
        thresholded = self.preprocess_image(image_to_process, ratio)
        found_contours, hierarchy = cv2.findContours(thresholded, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        classified = self._classify_contours_by_area(found_contours, hierarchy)
        contours = [ext_contour for (ext_contour, _) in classified]
        mask = self._create_mask(contours, image_to_process.shape)

        return mask, contours

    @staticmethod
    def preprocess_image(image, ratio=1, blur='median', method='multiotsu'):
        """
        Generic preprocessing using blur and adaptive thresholding
        """
        # Apply blur
        if blur == 'gaussian':
            blurred = cv2.GaussianBlur(image, (5, 5), 0)
        elif blur == 'median':
            blurred = cv2.medianBlur(image, 5)

        # Apply thresholding
        if method == 'otsu':
            otsu_threshold, _ = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            dynamic_threshold = otsu_threshold * ratio
            _, dynamic_thresh = cv2.threshold(blurred, dynamic_threshold, 255, cv2.THRESH_BINARY)

        elif method == 'multiotsu':
            thresholds = threshold_multiotsu(blurred, classes=3)
            t_high = thresholds[1] * ratio
            _, dynamic_thresh = cv2.threshold(blurred, t_high, 255, cv2.THRESH_BINARY)

        return dynamic_thresh

    @staticmethod
    def _classify_contours_by_area(contours, hierarchy, top_n=None):
        """
        Finds external contours and their internal contours, sorted by area in descending order.

        Args:
            contours (list): List of contours.
            hierarchy (numpy.ndarray): Contour hierarchy information.
            top_n (int, optional): Number of top external contours to return. If None, returns all.

        Returns:
            list: Tuples of (external_contour, internal_contours_list) sorted by external contour area.
        """
        # Map parent indices to their child contours
        parent_children_map = defaultdict(list)

        external_contours = []

        # Identify external contours and collect their largest internal
        for i in range(len(contours)):
            if hierarchy[0][i][3] == -1:  # External contour has no parent
                ext_contour = contours[i]
                area = cv2.contourArea(ext_contour)
                internal_contours = parent_children_map.get(i, [])
                # Find the largest internal contour if any
                largest_internal = None
                if internal_contours:
                    largest_internal = max(internal_contours, key=lambda c: cv2.contourArea(c))
                external_contours.append((area, ext_contour, largest_internal))

        # Sort by external contour area (descending)
        external_contours.sort(reverse=True, key=lambda x: x[0])

        # Apply top_n limit
        if top_n is not None:
            external_contours = external_contours[:top_n]

        # Return tuples (external_contour, largest_internal_contour)
        return [(ext, largest_internal) for (_, ext, largest_internal) in external_contours]

    @staticmethod
    def _create_mask(contours, image_shape):
        masks = []
        for contour in contours:
            mask = np.zeros(image_shape, dtype=np.uint8)
            if contour is not None:
                cv2.drawContours(mask, [contour], -1, 255, cv2.FILLED)
            masks.append(mask)
            # print(len(masks))
        return masks
