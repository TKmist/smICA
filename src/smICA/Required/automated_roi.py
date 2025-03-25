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
        self.all_external_masks = None
        self.all_internal_masks = None
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


    def detect_cell_roi(self, image_to_process, ratio, nucleus=False):
        """
        Znajduje ROI w obrazie i zapisuje wynik do atrybutu roi_image.
        """
        if image_to_process is None:
            raise ValueError("Obraz nie został załadowany. Użyj metody load_image().")

        # Preprocessing: rozmycie i progowanie
        thresholded = self._preprocess_image_dynamic(image_to_process, ratio)

        # Znajdowanie konturów
        contours, hierarchy = cv2.findContours(thresholded, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        if not contours or hierarchy is None:
            raise ValueError("Nie znaleziono konturów w obrazie.")
            #external_mask = self._create_external_mask(None, image_to_process.shape)
        else:
            # Klasyfikacja konturów
            classified_contours = self._classify_contours_by_area(contours, hierarchy)

            external = [ext_contour for (ext_contour, _) in classified_contours]

            internal = [int_contour for (_, int_contour) in classified_contours]

            # Tworzenie maski zewnętrznego konturu
            external_masks = self._create_mask(external, internal, image_to_process.shape)

            internal_masks = self._create_mask(internal, internal, image_to_process.shape)

            self.all_contours = list(external)
            self.all_external_masks = list(external_masks)
            self.all_internal_masks = list(internal_masks)

        #return external_mask

    def detect_nucleus_roi(self, original_image, cell_roi, ratio):

        processed_image = cv2.bitwise_not(original_image) * (cell_roi).astype(int)
        # print(processed_image)
        processed_image = (processed_image * (255 / processed_image.max())).astype(np.uint8)

        nucleus_roi = self.detect_cell_roi(processed_image, ratio)
        return nucleus_roi

    def make_full_roi(self, cell_roi, nucleus_roi):

        full_mask = cell_roi - nucleus_roi
        return full_mask

    def save_roi(self):
        """
        Zapisuje wynikowy obraz ROI do wyjściowej ścieżki.
        """
        if self.roi_image is None:
            raise ValueError("ROI nie zostało wykryte. Użyj metody detect_roi().")
        cv2.imwrite(self.output_path, self.roi_image * 255)

        formatted_array = np.where(self.roi_image == 0, '-', '1')
        np.savetxt(self.output_path.replace('.png', '.dat'), formatted_array, fmt='%s', delimiter='\t')

        return 0

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

    # @staticmethod
    # def _classify_contours_by_area(contours, hierarchy):
    #     largest_external_contour = None
    #     largest_external_area = 0
    #     corresponding_internal_contour = None
    #
    #     for i in range(len(contours)):
    #         # Sprawdź, czy kontur jest zewnętrzny (brak rodzica)
    #         if hierarchy[0][i][3] == -1:
    #             area = cv2.contourArea(contours[i])
    #             # Jeśli ten kontur jest większy niż poprzednio znaleziony
    #             if area > largest_external_area:
    #                 largest_external_contour = contours[i]
    #                 largest_external_area = area
    #
    #                 # Szukamy wewnętrznego konturu dla tego zewnętrznego konturu
    #                 corresponding_internal_contour = None
    #                 for j in range(len(contours)):
    #                     # Jeśli kontur `j` ma `i` jako rodzica
    #                     if hierarchy[0][j][3] == i:
    #                         corresponding_internal_contour = contours[j]
    #                         break  # Bierzemy pierwszy wewnętrzny kontur, jeśli istnieje
    #
    #     return largest_external_contour, corresponding_internal_contour

    # @staticmethod
    # def _classify_contours_by_area(contours, hierarchy):
    #     # List to store the largest contours and their corresponding internal contours
    #     largest_contours = []
    #
    #     for i in range(len(contours)):
    #         # Check if the contour is external (no parent)
    #         if hierarchy[0][i][3] == -1:
    #             area = cv2.contourArea(contours[i])
    #             # If this contour is larger than the smallest in our list, replace it
    #             if len(largest_contours) < 2:
    #                 largest_contours.append((area, contours[i], None))
    #             else:
    #                 # Find the smallest area in the list
    #                 min_area_index = min(range(len(largest_contours)), key=lambda x: largest_contours[x][0])
    #                 if area > largest_contours[min_area_index][0]:
    #                     largest_contours[min_area_index] = (area, contours[i], None)
    #
    #             # Sort the list to keep the largest contours at the top
    #             largest_contours.sort(reverse=True, key=lambda x: x[0])
    #
    #
    #             # Find the corresponding internal contour for the largest external contours
    #             # for j in range(len(largest_contours)):
    #             #     if largest_contours[j][2] is None:
    #             #         for k in range(len(contours)):
    #             #             if hierarchy[0][k][3] == i:
    #             #                 largest_contours[j] = (largest_contours[j][0], largest_contours[j][1], contours[k])
    #             #                 break  # Take the first internal contour if it exists
    #
    #     # Return the two largest external contours and their corresponding internal contours
    #     #return [(contour, internal) for (area, contour, internal) in largest_contours]
    #     return largest_contours

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

        # Identify external contours and collect their internals
        for i in range(len(contours)):
            if hierarchy[0][i][3] == -1:  # External contour has no parent
                ext_contour = contours[i]
                area = cv2.contourArea(ext_contour)
                # Get direct internal contours (immediate children)
                internal_contours = parent_children_map.get(i, [])
                external_contours.append((area, ext_contour, internal_contours))

        # Sort by external contour area (descending)
        external_contours.sort(reverse=True, key=lambda x: x[0])

        # Apply top_n limit
        if top_n is not None:
            external_contours = external_contours[:top_n]

        # Return (external_contour, internal_contours_list) tuples
        return [(ext, internals) for (_, ext, internals) in external_contours]

    @staticmethod
    def _create_mask(contours, image_shape):
        masks = []
        for contour in contours:
            mask = np.zeros(image_shape, dtype=np.uint8)
            if contour is not None:
                cv2.drawContours(mask, [contour], -1, 255, cv2.FILLED)
            masks.append(mask)
            print(len(masks))
        return masks

    # @staticmethod
    # def _create_final_mask(external_mask, ellipse_mask, image_shape):
    #     mask_between = cv2.bitwise_and(external_mask, cv2.bitwise_not(ellipse_mask))
    #     final_mask = np.zeros(image_shape, dtype=np.uint8)
    #     final_mask[mask_between == 255] = 1
    #     return final_mask
