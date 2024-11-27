import argparse
from recipify.preprocessing import preprocess_image
from recipify.ocr import extract_text
from recipify.extraction import parse_receipt_data

def main(image_path):
    # Step 1: Preprocess the image
    print("Preprocessing the image...")
    preprocessed_image = preprocess_image(image_path)
    print("Preprocessed image created.")

    # Step 2: Extract text using OCR
    print("Running OCR...")
    raw_text = extract_text(preprocessed_image)
    print(f"Raw OCR Text:\n{raw_text}")

    if not raw_text.strip():  # If OCR text is empty
        print("OCR did not extract any text from the image.")
    
    # Step 3: Parse receipt data
    print("Extracting receipt data...")
    extracted_data = parse_receipt_data(raw_text)
    
    if not extracted_data:  # If no data is extracted
        print("No data was extracted from the receipt.")
        return
    
    # Step 4: Display the extracted data
    print("\nDetected Shop:", extracted_data.get("vendor", "Unknown"))
    print("Total Amount:", extracted_data.get("total", "Unknown"))
    print("Date:", extracted_data.get("date", "Unknown"))
    
    # Display the items if they exist
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
    args = parser.parse_args()
    main(args.image)
