import re

def classify_receipt(text):
    """
    Classifies the receipt type based on the OCR-extracted text.

    Args:
        text (str): The OCR-extracted text from the receipt.

    Returns:
        str: The type of the receipt ("Walmart", "Cafeteria", or "Unknown").
    """
    try:
        # Check for keywords unique to Walmart receipts
        if re.search(r"\bWalmart\b", text, re.IGNORECASE):
            return "Walmart"

        # Check for keywords unique to Cafeteria receipts
        if re.search(r"\bCafeteria\b", text, re.IGNORECASE):
            return "Cafeteria"

        # Default to "Unknown" if no keywords match
        return "Unknown"

    except Exception as e:
        raise RuntimeError(f"Error classifying receipt: {e}")
