from recipify.classification import load_model, detect_receipt_elements
from recipify.extraction import parse_receipt_data

# Load the trained YOLO model
model = load_model("saved_models/yolov5_best.pt")

# Path to the receipt image
image_path = "dataset/images/0.jpg"

# Detect receipt elements (with or without preprocessing)
detections = detect_receipt_elements(model, image_path, preprocess_for_detection=True)
print("Detections:", detections)

# Now parse the OCR text
ocr_text = "TOTAL PURCHASE 49.90 Walmart"  # This would normally come from OCR
parsed_data = parse_receipt_data(ocr_text)
print("Parsed Data:", parsed_data)
