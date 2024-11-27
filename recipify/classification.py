import joblib

# Load the trained model and vectorizer
model = joblib.load("saved_models/receipt_classifier.pkl")
vectorizer = joblib.load("saved_models/vectorizer.pkl")

def classify_receipt(text):
    """
    Classifies a receipt based on its OCR text.

    Args:
        text (str): The OCR-extracted text from the receipt.

    Returns:
        str: The predicted receipt type.
    """
    text_transformed = vectorizer.transform([text])
    receipt_type = model.predict(text_transformed)[0]
    return receipt_type
