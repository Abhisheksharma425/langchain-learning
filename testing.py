"""
OCR Analysis Script
This script performs OCR (Optical Character Recognition) on images
"""

import os
from PIL import Image
import pytesseract
from pathlib import Path


class OCRAnalyzer:
    """Class to handle OCR analysis on images"""
    
    def __init__(self, tesseract_path=None):
        """
        Initialize OCR Analyzer
        
        Args:
            tesseract_path: Path to tesseract executable (optional)
        """
        if tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
    
    def extract_text(self, image_path, lang='eng'):
        """
        Extract text from an image
        
        Args:
            image_path: Path to the image file
            lang: Language for OCR (default: 'eng')
            
        Returns:
            Extracted text as string
        """
        try:
            # Open the image
            image = Image.open(image_path)
            
            # Perform OCR
            text = pytesseract.image_to_string(image, lang=lang)
            
            return text.strip()
        
        except Exception as e:
            return f"Error processing image: {str(e)}"
    
    def extract_text_with_confidence(self, image_path, lang='eng'):
        """
        Extract text with confidence scores
        
        Args:
            image_path: Path to the image file
            lang: Language for OCR (default: 'eng')
            
        Returns:
            Dictionary containing text and confidence data
        """
        try:
            image = Image.open(image_path)
            
            # Get detailed OCR data
            data = pytesseract.image_to_data(image, lang=lang, output_type=pytesseract.Output.DICT)
            
            return data
        
        except Exception as e:
            return {"error": str(e)}
    
    def analyze_directory(self, directory_path, lang='eng'):
        """
        Analyze all images in a directory
        
        Args:
            directory_path: Path to directory containing images
            lang: Language for OCR (default: 'eng')
            
        Returns:
            Dictionary with filename as key and extracted text as value
        """
        results = {}
        image_extensions = {'.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif'}
        
        directory = Path(directory_path)
        
        for file_path in directory.iterdir():
            if file_path.suffix.lower() in image_extensions:
                text = self.extract_text(str(file_path), lang=lang)
                results[file_path.name] = text
        
        return results


def main():
    """Main function to demonstrate OCR analysis"""
    
    # Initialize OCR Analyzer
    # If using Windows, you might need to specify tesseract path:
    # analyzer = OCRAnalyzer(tesseract_path=r'C:\Program Files\Tesseract-OCR\tesseract.exe')
    analyzer = OCRAnalyzer()
    
    # Example 1: Extract text from a single image
    print("=" * 50)
    print("OCR Analysis Example")
    print("=" * 50)
    
    image_path = input("Enter the path to an image file (or press Enter to skip): ").strip()
    
    if image_path and os.path.exists(image_path):
        print(f"\nAnalyzing: {image_path}")
        text = analyzer.extract_text(image_path)
        print(f"\nExtracted Text:\n{text}")
        
        # Get confidence data
        data = analyzer.extract_text_with_confidence(image_path)
        if "error" not in data:
            confidences = [conf for conf in data['conf'] if conf != -1]
            if confidences:
                avg_confidence = sum(confidences) / len(confidences)
                print(f"\nAverage Confidence: {avg_confidence:.2f}%")
    
    # Example 2: Analyze directory
    directory_path = input("\nEnter a directory path to analyze all images (or press Enter to skip): ").strip()
    
    if directory_path and os.path.exists(directory_path):
        print(f"\nAnalyzing directory: {directory_path}")
        results = analyzer.analyze_directory(directory_path)
        
        for filename, text in results.items():
            print(f"\n--- {filename} ---")
            print(text[:200] + "..." if len(text) > 200 else text)


if __name__ == "__main__":
    main()
