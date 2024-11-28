import argparse
from recipify.preprocessing import preprocess_image
from recipify.ocr import extract_text
from recipify.extraction import parse_receipt_data
from ultralytics import YOLO  # YOLOv11

def load_yolo_model(weights_path):
    """
    Load the YOLOv11 model.
    """
    return YOLO(weights_path)

def detect_receipt_elements(model, image_path):
    """
    Detects receipt elements using YOLOv11.

    Args:
        model: Loaded YOLO model.
        image_path (str): Path to the receipt image.

    Returns:
        list[dict]: Detected elements with labels and bounding boxes.
    """
    results = model(image_path)
    detections = []
    for box in results.boxes:
        detections.append({
            "label": results.names[int(box.cls[0])],
            "confidence": box.conf[0].item(),
            "coordinates": box.xyxy[0].tolist()  # [x1, y1, x2, y2]
        })
    return detections

def main(image_path, yolo_weights):
    # Step 1: Preprocess the image
    print("Preprocessing the image...")
    preprocessed_image = preprocess_image(image_path)
    print("Preprocessed image created.")

    # Step 2: Detect elements using YOLO
    print("Running YOLOv8 detection...")
    model = load_yolo_model(yolo_weights)
    detections = detect_receipt_elements(model, image_path)
    print(f"Detections: {detections}")

    # Step 3: Extract text using OCR
    print("Running OCR...")
    raw_text = extract_text(preprocessed_image)
    print(f"Raw OCR Text:\n{raw_text}")

    if not raw_text.strip():
        print("OCR did not extract any text from the image.")
        return

    # Step 4: Parse receipt data
    print("Extracting receipt data...")
    extracted_data = parse_receipt_data(raw_text)

    # Step 5: Display the extracted data
    print("\nDetected Shop:", extracted_data.get("vendor", "Unknown"))
    print("Total Amount:", extracted_data.get("total", "Unknown"))
    print("Date:", extracted_data.get("date", "Unknown"))
    if "items" in extracted_data and extracted_data["items"]:
        print("Items:")
        for item in extracted_data["items"]:
            name = item.get("name", "Unknown Item")
            price = item.get("price", "Unknown Price")
            print(f"- {name}: ${price}")
    else:
        print("No items detected.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Receipt Scanner Demo")
    parser.add_argument("--image", type=str, required=True, help="Path to the receipt image")
    parser.add_argument("--weights", type=str, required=True, help="Path to the YOLOv8 model weights")
    args = parser.parse_args()
    main(args.image, args.weights)
