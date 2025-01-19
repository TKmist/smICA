import os
import cv2
import numpy as np
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
        self.all_hierarchy = None
        

    def load_image(self):
        """
        Wczytuje obraz z podanej ścieżki.
        """
        # self.image = cv2.imread(self.input_path, cv2.IMREAD_GRAYSCALE)

        loaded_image = np.load(self.input_path)

        # self.image = (loaded_image * (255 / loaded_image.max())).astype(np.uint8)

        if self.image is None:
            raise FileNotFoundError(f"Nie udało się wczytać obrazu: {self.input_path}")

    def detect_roi(self):
        """
        Znajduje ROI w obrazie i zapisuje wynik do atrybutu roi_image.
        """
        if self.image is None:
            raise ValueError("Obraz nie został załadowany. Użyj metody load_image().")
        image = self.image.astype(np.float32)
        # Preprocessing: rozmycie i progowanie
        thresholded = self._preprocess_image(self.image)

        # Znajdowanie konturów
        contours, hierarchy = cv2.findContours(thresholded, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        if not contours or hierarchy is None:
            raise ValueError("Nie znaleziono konturów w obrazie.")

        # Klasyfikacja konturów
        external_contour, internal_contour = self._classify_contours_by_area(contours, hierarchy)

        # Dopasowanie elipsy i stworzenie maski ROI
        ellipse_mask = np.zeros(self.image.shape, dtype=np.uint8)
        if self.find_nucleus and internal_contour is not None:
            ellipse_mask, _ = self._fit_ellipse_to_contour(internal_contour, self.image.shape)

        # Tworzenie maski zewnętrznego konturu
        external_mask = self._create_external_mask(external_contour, self.image.shape)

        # Łączenie masek w finalną ROI
        self.roi_image = self._create_final_mask(external_mask, ellipse_mask, self.image.shape)
        self.all_contours = contours
        self.all_hierarchy = hierarchy

    def detect_cell_roi(self,image_to_process,ratio):
        """
        Znajduje ROI w obrazie i zapisuje wynik do atrybutu roi_image.
        """
        
        if image_to_process is None:
            raise ValueError("Obraz nie został załadowany. Użyj metody load_image().")
        image_to_process = np.clip((image_to_process/np.max(image_to_process))*255 ,0,255).astype(np.uint8)   
        # image_to_process = np.clip(image_to_process,0,255).astype(np.uint8)
        # Preprocessing: rozmycie i progowanie
        thresholded = self._preprocess_image_dynamic(image_to_process,ratio)

        # Znajdowanie konturów
        # thresholded_uint8 = np.clip(thresholded, 0, 255).astype(np.uint8)
        contours, hierarchy = cv2.findContours(thresholded, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        if not contours or hierarchy is None:
            # raise ValueError("Nie znaleziono konturów w obrazie.")
            external_mask = self._create_external_mask(None, image_to_process.shape)
        else:
        # Klasyfikacja konturów
            external_contour, internal_contour = self._classify_contours_by_area(contours, hierarchy)

        # Dopasowanie elipsy i stworzenie maski ROI
        # ellipse_mask = np.zeros(image_to_processshape, dtype=np.uint8)
        # if self.find_nucleus and internal_contour is not None:
        #     ellipse_mask, _ = self._fit_ellipse_to_contour(internal_contour, image_to_process.shape)

        # Tworzenie maski zewnętrznego konturu
            external_mask = self._create_external_mask(external_contour, image_to_process.shape)

        # Łączenie masek w finalną ROI
        # roi_image = self._create_final_mask(external_mask, ellipse_mask, image_to_process.shape)
        # self.all_contours = contours
        # self.all_hierarchy = hierarchy

        return external_mask

    def detect_nucleus_roi(self,original_image,cell_roi,ratio):
        
        processed_image = cv2.bitwise_not(original_image)*(cell_roi).astype(int)
        # print(processed_image)
        processed_image = (processed_image * (255 / processed_image.max())).astype(np.uint8)
        
        nucleus_roi = self.detect_cell_roi(processed_image,ratio)
        return nucleus_roi

    def make_full_roi(self,cell_roi,nucleus_roi):
        
        full_mask = cell_roi-nucleus_roi
        return full_mask
        
    # def invert_and_apply_mask(self):
    #     """
    #     Inverts the ROI mask and applies it to make the mask transparent where the mask is black and non-transparent where the mask is white.
    #     """
    #     if self.roi_image is None:
    #         raise ValueError("ROI mask is not available. Ensure detect_roi() was called successfully.")
    
    #     # Invert the ROI mask: 0 becomes 255, and 255 becomes 0
    #     inverted_mask = cv2.bitwise_not(self.roi_image)

    #     return inverted_mask

        
    def save_roi(self):
        """
        Zapisuje wynikowy obraz ROI do wyjściowej ścieżki.
        """
        if self.roi_image is None:
            raise ValueError("ROI nie zostało wykryte. Użyj metody detect_roi().")
        cv2.imwrite(self.output_path, self.roi_image * 255)

        formatted_array = np.where(self.roi_image == 0, '-', '1')
        np.savetxt(self.output_path.replace('.png', '.dat'), formatted_array, fmt='%s', delimiter='\t')

    def founded_roi_test(self):

        roi_too_small = np.sum(self.roi_image, axis=(0, 1)) < 2500
        too_many_shapes = len(self.all_contours) > 10

        if too_many_shapes or roi_too_small:
            print(f'The {self.input_path} might be wrong. Please check it!')

            return 1

        return 0

    @staticmethod
    def _preprocess_image(image):
        """
        Preprocess the image: reduce noise, blure and apply thresholding.
        """

        # Step 2: Apply Gaussian blur for noise reduction
        
        blurred = cv2.GaussianBlur(image, (5, 5), 0)

        # Step 3: Adaptive thresholding or Otsu's method
        _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        return thresh

    @staticmethod
    def _preprocess_image_dynamic(image,ratio):
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
    def _classify_contours_by_area(contours, hierarchy):
        largest_external_contour = None
        largest_external_area = 0
        corresponding_internal_contour = None

        for i in range(len(contours)):
            # Sprawdź, czy kontur jest zewnętrzny (brak rodzica)
            if hierarchy[0][i][3] == -1:
                area = cv2.contourArea(contours[i])
                # Jeśli ten kontur jest większy niż poprzednio znaleziony
                if area > largest_external_area:
                    largest_external_contour = contours[i]
                    largest_external_area = area

                    # Szukamy wewnętrznego konturu dla tego zewnętrznego konturu
                    corresponding_internal_contour = None
                    for j in range(len(contours)):
                        # Jeśli kontur `j` ma `i` jako rodzica
                        if hierarchy[0][j][3] == i:
                            corresponding_internal_contour = contours[j]
                            break  # Bierzemy pierwszy wewnętrzny kontur, jeśli istnieje

        return largest_external_contour, corresponding_internal_contour

    @staticmethod
    def _fit_ellipse_to_contour(internal_contour, image_shape):
        if internal_contour is not None and len(internal_contour) >= 5:
            internal_ellipse = cv2.fitEllipse(internal_contour)
            ellipse_mask = np.zeros(image_shape, dtype=np.uint8)
            center = tuple(map(int, internal_ellipse[0]))
            axes = (int(internal_ellipse[1][0] / 2), int(internal_ellipse[1][1] / 2))
            cv2.ellipse(ellipse_mask, center, axes, internal_ellipse[2], 0, 360, 255, -1)
            return ellipse_mask, internal_ellipse
        return np.zeros(image_shape, dtype=np.uint8), None

    @staticmethod
    def _create_external_mask(external_contour, image_shape):
        external_mask = np.zeros(image_shape, dtype=np.uint8)
        if external_contour is not None:
            cv2.drawContours(external_mask, [external_contour], -1, 255, cv2.FILLED)
        return external_mask

    @staticmethod
    def _create_final_mask(external_mask, ellipse_mask, image_shape):
        mask_between = cv2.bitwise_and(external_mask, cv2.bitwise_not(ellipse_mask))
        final_mask = np.zeros(image_shape, dtype=np.uint8)
        final_mask[mask_between == 255] = 1
        return final_mask


def process_images(base_path, input_folder, output_folder, nucleus_files):
    """
    Przetwarza wszystkie obrazy .png w podanym katalogu wejściowym i zapisuje wyniki w katalogu wyjściowym.
    """

    # Upewnij się, że folder wyjściowy istnieje
    os.makedirs(output_folder, exist_ok=True)

    # Pobierz pliki .png
    npy_files = [f for f in os.listdir(input_folder) if f.endswith('.npy')]

    if not npy_files:
        print(f"No .npy files in: {input_folder}")
        return

    for file in tqdm(npy_files):
        input_path = os.path.join(input_folder, file)
        output_path = os.path.join(output_folder, file.replace('.npy', '.png'))

        if nucleus_files in file:
            find_nucleus = True
        else:
            find_nucleus = False

        # Przetwarzanie obrazów przy użyciu klasy
        try:
            processor = ImageROIProcessor(input_path, output_path, find_nucleus)
            processor.load_image()
            processor.detect_roi()
            processor.save_roi()
            processor.founded_roi_test()
        except Exception as error:
            print(f"Error while processing {file}: {error}")


if __name__ == '__main__':
    # Wywołanie przetwarzania
    base_path = './autoROI/TRAIN_DATA/'

    input_folder = os.path.join(base_path, 'npy')
    output_folder = os.path.join(base_path, 'znalezione_ROI')

    process_images(base_path, input_folder, output_folder, 'ch_2')
