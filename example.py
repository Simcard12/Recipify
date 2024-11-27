from recipify.preprocessing import preprocess_image
from recipify.ocr import extract_text
from recipify.extraction import parse_receipt_data
import cv2

# Path to the receipt image
image_path = "examples/5.jpg"

# Step 1: Preprocess the receipt image
print("Preprocessing the receipt image...")
preprocessed_image = preprocess_image(image_path)

# Save and inspect the preprocessed image
cv2.imwrite("preprocessed_receipt_5.jpg", preprocessed_image)
print("Preprocessed image saved as 'preprocessed_receipt.jpg'.")

# Step 2: Perform OCR on the preprocessed image
print("Extracting text using OCR...")
ocr_text = extract_text(preprocessed_image)
print(f"Raw OCR Text:\n{ocr_text}")  # Debug: Check OCR output

# Step 3: Parse receipt data from the extracted text
print("Parsing receipt data...")
parsed_data = parse_receipt_data(ocr_text)
print(f"Extracted Data: {parsed_data}")
