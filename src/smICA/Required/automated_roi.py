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
from tqdm import tqdm
import pickle


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
        self.all_contours = None
        self.all_masks = None
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


    def detect_cell_roi(self, image_to_process, ratio, find_nucleus=False):
        """
        Znajduje ROI w obrazie i zapisuje wynik do atrybutu roi_image.
        """

        # Preprocessing: rozmycie i progowanie
        thresholded = self._preprocess_image_dynamic(image_to_process, ratio)

        # Znajdowanie konturów
        found_contours, hierarchy = cv2.findContours(thresholded, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)


        classified_contours_hierarchy = self._classify_contours_by_area(found_contours, hierarchy)

        # Tworzenie maski zewnętrznego konturu

        if find_nucleus:
            # Generate masks for nucleus ROI
            self.all_masks = self.detect_nucleus_roi(classified_contours_hierarchy, image_to_process.shape)
        else:
            # Use only external contours
            found_contours = [ext_contour for (ext_contour, _) in classified_contours_hierarchy]
            self.all_masks = self._create_mask(found_contours, image_to_process.shape)

        self.all_contours = [ext_contour for (ext_contour, _) in classified_contours_hierarchy]

    def detect_nucleus_roi(self, classified_contours, image_shape):
        """
        Creates masks between each external contour and its largest internal contour.

        Args:
            classified_contours (list): List of tuples (external_contour, largest_internal_contour).
            image_shape (tuple): Shape of the image to create masks of the same size.

        Returns:
            list: Generated masks for each external-internal contour pair.
        """
        masks = []
        for ext_contour, largest_internal in classified_contours:
            # Create a blank mask
            mask = np.zeros(image_shape[:2], dtype=np.uint8)
            # Draw the external contour filled
            cv2.drawContours(mask, [ext_contour], -1, 255, cv2.FILLED)
            if largest_internal is not None:
                # Subtract the largest internal contour
                cv2.drawContours(mask, [largest_internal], -1, 0, cv2.FILLED)
            masks.append(mask)
        return masks


    @staticmethod
    def _preprocess_image_dynamic(image, ratio):
        """
        Preprocess the image: reduce noise, blure and apply thresholding.
        """

        # Step 2: Apply Gaussian blur for noise reduction
        blurred = cv2.GaussianBlur(image, (5, 5), 0)

        # Step 3: Adaptive thresholding or Otsu's method
        _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Optional: Modify the threshold dynamically based on the Otsu result
        # If you want to increase or decrease the threshold level
        dynamic_threshold = _ * ratio  # Example: Increase the threshold by 20%
        _, dynamic_thresh = cv2.threshold(blurred, dynamic_threshold, 255, cv2.THRESH_BINARY)

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
        for j, h in enumerate(hierarchy[0]):
            parent_idx = h[3]
            parent_children_map[parent_idx].append(contours[j])

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


