# **Recipify**

**Recipify** is a receipt data extraction system designed to process receipt images and extract key details such as vendor name, total amount, items, and date/time. The project leverages **YOLOv5** for object detection and **Tesseract OCR** for text recognition, combining the two to handle receipts of varying formats.

---

## **Features**
- **Image Preprocessing**: Enhances receipt images for improved OCR accuracy.
- **Object Detection**: Uses YOLOv5 to detect receipt elements such as the shop name, total, items, and date/time.
- **Text Recognition**: Extracts text from receipts using Tesseract OCR.
- **Receipt Classification**: Automatically classifies receipts into predefined types (e.g., Walmart, Cafeteria).
- **Data Parsing**: Parses and organizes extracted information into structured data.

---

## **Setup and Installation**

### **1. Clone the Repository**
```bash
git clone https://github.com/subhashhhhhh/Recipify.git
cd Recipify
```

### **2. Set Up a Virtual Environment**
Create and activate a Python virtual environment:
```bash
python -m venv recipify_env
source recipify_env/bin/activate  # On Windows: recipify_env\Scripts\activate
```

### **3. Install Dependencies**
Install the required Python packages:
```bash
pip install -r requirements.txt
```

### **4. Download YOLOv5**
Clone the YOLOv5 repository into the project directory:
```bash
git clone https://github.com/ultralytics/yolov5.git
cd yolov5
pip install -r requirements.txt
cd ..
```

---

## **Usage**

### **1. Prepare the Dataset**
If you want to train YOLOv5 on your dataset:
1. Organize your dataset as follows:
   ```
   dataset/
   ├── train/
   │   ├── images/
   │   └── labels/
   ├── val/
   │   ├── images/
   │   └── labels/
   ```
2. Update the `dataset.yaml` file in the YOLOv5 folder with paths to your dataset.

### **2. Train the YOLOv5 Model**
Train the YOLOv5 model on your dataset:
```bash
python yolov5/train.py --data dataset.yaml --cfg yolov5s.yaml --weights yolov5s.pt --epochs 50
```

### **3. Run the Demo**
To process a receipt image and extract data:
```bash
python demo.py --image <path_to_receipt_image>
```

Example:
```bash
python demo.py --image example_receipt.jpg
```

**Output**: A structured JSON-like summary of the receipt details will be displayed.

---

## **Folder Structure**
```
Recipify/
├── recipify/
│   ├── __init__.py
│   ├── preprocessing.py      # Image preprocessing code
│   ├── ocr.py                # Text extraction using Tesseract
│   ├── classification.py     # Classifies receipt type (e.g., Walmart, Cafeteria)
│   ├── extraction.py         # Parses receipt data based on type
│   └── dataset_processing.py # Converts annotated datasets for YOLOv5
├── yolov5/                   # YOLOv5 model
├── dataset/                  # Dataset for YOLOv5 (images and labels)
├── examples/                 # Example scripts and sample images
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
```

---

## **Dependencies**
- **Python 3.9+**
- **OpenCV**: For image preprocessing.
- **Tesseract OCR**: For text recognition.
- **YOLOv5**: For object detection.
- **PyTorch**: For training and inference.

---

## **Acknowledgments**
- **YOLOv5**: Ultralytics for the object detection framework.
- **Tesseract OCR**: Google for the text recognition engine.
- Various open-source datasets for receipts.

---

## **Contributing**
Contributions are welcome! If you want to improve the project:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m "Add feature"`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.

---

## **License**
This project is licensed under the [MIT License](LICENSE).
