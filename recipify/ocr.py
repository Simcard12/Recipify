import pytesseract

def extract_text(image):
    """
    Extracts text from the preprocessed image using OCR.

    Args:
      image: A preprocessed image.

    Returns:
      Extracted text as a string.
    """
    try:
        # Use Pytesseract to perform OCR with improved configs
        text = pytesseract.image_to_string(image, lang='eng', config='--psm 4 --oem 3')
        return text
    except Exception as e:
        raise RuntimeError(f"Error in extract_text: {e}")
