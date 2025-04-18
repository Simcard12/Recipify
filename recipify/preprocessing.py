import cv2
import numpy as np

def preprocess_image(image_path):
    """
    Preprocesses the receipt image for OCR.

    Args:
      image_path: Path to the receipt image.

    Returns:
      A preprocessed image.
    """
    try:
        # 1. Load the image
        image = cv2.imread(image_path)

        # 2. Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # 3. Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (3, 3), 1)

        # 4. Use Adaptive Thresholding or Otsu's Binarization
        # Try adaptive thresholding
        #binary = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                       #cv2.THRESH_BINARY, 11, 2)

        # Alternatively, you can use Otsu's method if adaptive thresholding doesn't work well
        _, binary = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # 5. Use morphology to enhance text regions
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
        processed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

        return processed
    except Exception as e:
        raise RuntimeError(f"Error in preprocess_image: {e}")
