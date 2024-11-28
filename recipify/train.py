from ultralytics import YOLO

# Load a pre-trained model
model = YOLO("yolo11n.pt")  # Use the YOLOv11 nano version (smallest model, better for training)

# Train the model
model.train(data='/Users/subhashgottumukkala/Developer/GitHub/Recipify/recipify/dataset.yaml', epochs=100, imgsz=640, device="mps")  # Adjust settings as needed
