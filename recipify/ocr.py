import pytesseract
import re

def detect_total_amount(text):
    """
    Check if the total amount can be extracted from the OCR text.
    
    Args:
        text (str): OCR-extracted text.
    
    Returns:
        float: Extracted total amount or None if not found.
    """
    total_match = re.search(r"TOTAL\s*[:\-]?\s*\$?([\d.]+)", text, re.IGNORECASE)
    if total_match:
        return float(total_match.group(1))
    return None

def extract_text(image):
    """
    Extracts text from the preprocessed image using OCR with dynamic PSM selection.
    
    Args:
        image: A preprocessed image.
    
    Returns:
        str: The extracted text.
    """
    try:
        # Try PSM 6
        custom_config_psm6 = r'--oem 3 --psm 6'
        text_psm6 = pytesseract.image_to_string(image, lang='eng', config=custom_config_psm6)
        total_psm6 = detect_total_amount(text_psm6)

        # Try PSM 11
        custom_config_psm11 = r'--oem 3 --psm 11'
        text_psm11 = pytesseract.image_to_string(image, lang='eng', config=custom_config_psm11)
        total_psm11 = detect_total_amount(text_psm11)

        # Choose the PSM mode based on which successfully extracts the total
        if total_psm6 is not None:
            print("Using PSM 6 because total amount was detected.")
            return text_psm6
        elif total_psm11 is not None:
            print("Using PSM 11 because total amount was detected.")
            return text_psm11
        else:
            print("No total amount detected in either PSM mode.")
            return text_psm6  # Fallback to PSM 6 if both fail

    except Exception as e:
        raise RuntimeError(f"Error in extract_text: {e}")
