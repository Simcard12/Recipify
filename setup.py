from setuptools import setup, find_packages

setup(
    name='recipify',
    version='0.2.0',
    packages=find_packages(),
    install_requires=[
        'opencv-python',         # For image preprocessing
        'pytesseract',           # For OCR text extraction
        'numpy',                 # For numerical operations
        'pandas',                # For data handling (if used in results)
        'ultralytics',           # For YOLOv11 object detection
        'spacy',                 # For NLP (if using NER or rule-based parsing)
        'torch',                 # PyTorch backend for YOLOv11
        'transformers',          # For advanced NLP models (if needed)
        'lxml',                  # For parsing XML in dataset_processing.py
    ],
    extras_require={
        'dev': ['pytest', 'flake8'],  # Development dependencies
    },
    entry_points={
        'console_scripts': [
            'recipify-demo=recipify.demo:main',  # Allow running demo.py as a CLI
        ],
    },
)
