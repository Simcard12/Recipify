import xml.etree.ElementTree as ET
import os
import cv2

def parse_annotations(xml_path, image_dir, output_dir):
    """
    Parses the annotations.xml file to extract bounding box data and labels.
    Converts bounding boxes into YOLO format (normalized coordinates).
    
    Args:
        xml_path (str): Path to the annotations.xml file.
        image_dir (str): Path to the directory containing images.
        output_dir (str): Directory to save the YOLO formatted label files.
        
    Returns:
        list[dict]: A list of dictionaries containing image paths, labels, and bounding boxes.
    """
    # Parse the XML file
    tree = ET.parse(xml_path)
    root = tree.getroot()
    
    # Make sure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    dataset = []
    
    # Loop over each image in the XML annotations
    for image in root.findall("image"):
        image_data = {}
        image_name = image.get("name")
        image_path = os.path.join(image_dir, image_name)

        # Store image information
        image_data["image_path"] = image_path
        image_data["width"] = int(image.get("width"))
        image_data["height"] = int(image.get("height"))
        image_data["annotations"] = []

        # Define the label file path directly in the output directory (not nested)
        label_file_path = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(image_name))[0]}.txt")

        # Open the label file for the current image
        with open(label_file_path, "w") as label_file:
            # Extract bounding boxes and labels
            for box in image.findall("box"):
                label = box.get("label")
                xtl = float(box.get("xtl"))  # Top-left X coordinate
                ytl = float(box.get("ytl"))  # Top-left Y coordinate
                xbr = float(box.get("xbr"))  # Bottom-right X coordinate
                ybr = float(box.get("ybr"))  # Bottom-right Y coordinate
                
                # Normalize the coordinates (YOLO format)
                width = image_data["width"]
                height = image_data["height"]
                
                # Normalized coordinates (relative to image size)
                center_x = (xtl + xbr) / 2 / width
                center_y = (ytl + ybr) / 2 / height
                box_width = (xbr - xtl) / width
                box_height = (ybr - ytl) / height

                # Class ID for each label (shop = 0, item = 1, total = 2, date_time = 3, receipt = 4)
                label_dict = {"shop": 0, "item": 1, "total": 2, "date_time": 3, "receipt": 4}
                class_id = label_dict.get(label.lower(), -1)  # Use lowercase for case-insensitivity
                
                if class_id != -1:
                    # Write to YOLO label file
                    label_file.write(f"{class_id} {center_x} {center_y} {box_width} {box_height}\n")
                
                # Add annotation for record
                image_data["annotations"].append({
                    "label": label,
                    "box": [xtl, ytl, xbr, ybr]
                })
        
        # Append image data to the dataset
        dataset.append(image_data)
    
    return dataset


# Example usage:
if __name__ == "__main__":
    # Replace these with the actual paths to your directories
    annotations_path = "dataset/annotations.xml"  # Path to your annotations.xml file
    images_dir = "dataset/images"  # Path to your images directory
    output_dir = "dataset/labels"  # Path to save YOLO labels (make sure this folder exists)

    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Parse the annotations and generate label files
    dataset = parse_annotations(annotations_path, images_dir, output_dir)

    # Print the first image's data (for verification)
    print(dataset[0])
