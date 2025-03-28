# **Recipify**

**Recipify** is a powerful receipt data extraction tool that combines **YOLO11** for object detection and **Tesseract OCR** for text recognition. It automatically extracts key information from receipt images, such as vendor names, total amounts, items, and dates, to help you keep track of your expenses.

[![CI](https://github.com/subhashhhhhh/Recipify/actions/workflows/ci.yml/badge.svg)](https://github.com/subhashhhhhh/Recipify/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/subhashhhhhh/Recipify/branch/main/graph/badge.svg)](https://codecov.io/gh/subhashhhhhh/Recipify)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## **Features**
- **YOLO11 Object Detection**: Detects receipt elements like shop names, total amounts, dates, and items
- **Tesseract OCR**: Extracts textual data from receipt images
- **Advanced Preprocessing**: Enhances image quality for better OCR and object detection
- **Multiple Receipt Types**: Supports Walmart, Cafeteria, and other receipt formats
- **Data Validation**: Ensures extracted data accuracy with Pydantic models
- **Comprehensive Logging**: Detailed logging with rotation and formatting
- **Type Safety**: Full type hints and runtime checking
- **Extensive Testing**: Comprehensive test suite with high coverage

## **Installation**

### **From PyPI**
```bash
pip install recipify
```

### **From Source**
```bash
git clone https://github.com/subhashhhhhh/Recipify.git
cd Recipify
pip install -e ".[dev]"  # Install with development dependencies
```

## **Quick Start**

```python
from recipify import parse_receipt_data

# Extract data from receipt text
receipt_text = """
Walmart
Apple          1.99
Banana         0.99
TOTAL          2.98
03/15/24
14:30
"""

result = parse_receipt_data(receipt_text)
print(result)
```

## **Development Setup**

1. **Create Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install Dependencies**
```bash
pip install -e ".[dev]"
```

3. **Setup Pre-commit Hooks**
```bash
pre-commit install
```

4. **Run Tests**
```bash
pytest
```

## **Configuration**

Recipify can be configured using environment variables:

```bash
export RECIPIFY_LOG_LEVEL=DEBUG
export RECIPIFY_TESSERACT_CMD=/usr/local/bin/tesseract
```

See `recipify/config/settings.py` for all available settings.

## **Contributing**

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
```bash
pytest
pre-commit run --all-files
```
5. Submit a pull request

## **License**
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## **Acknowledgments**
- Ultralytics for YOLO11
- Google for Tesseract OCR
- The Python community for excellent tools and libraries
