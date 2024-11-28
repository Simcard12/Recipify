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
        model: Loaded YOLOv11 model.
        image_path (str): Path to the receipt image.

    Returns:
        list[dict]: Detected elements with labels and bounding boxes.
    """
    # Run inference
    results = model(image_path)  # Returns a list of Results objects
    
    # Check if results are non-empty
    if not results:
        print("No detections.")
        return []

    # YOLOv11 returns a list; process the first result
    result = results[0]
    
    detections = []
    if hasattr(result, "boxes"):
        for box in result.boxes:
            detections.append({
                "label": result.names[int(box.cls[0])],  # Class label
                "confidence": box.conf[0].item(),        # Confidence score
                "coordinates": box.xyxy[0].tolist()      # Bounding box coordinates
            })
    else:
        print("No bounding boxes found in results.")
    
    return detections

def main(image_path, yolo_weights):
    # Step 1: Preprocess the image
    print("Preprocessing the image...")
    preprocessed_image = preprocess_image(image_path)
    print("Preprocessed image created.")

    # Step 2: Detect elements using YOLO
    print("Running YOLOv11 detection...")
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
    parser.add_argument("--weights", type=str, required=True, help="Path to the YOLOv11 model weights")
    args = parser.parse_args()
    main(args.image, args.weights)
