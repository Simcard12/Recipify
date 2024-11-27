from setuptools import setup, find_packages

setup(
    name='recipify',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'opencv-python',
        'pytesseract',
        'imutils',
        'numpy',
        'pandas',
    ],
)