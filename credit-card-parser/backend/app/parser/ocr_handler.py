"""
OCR fallback for scanned PDFs using Tesseract
"""
import pytesseract
from pdf2image import convert_from_path
from PIL import Image, ImageEnhance
import logging
import os

logger = logging.getLogger(__name__)

# Configure Tesseract path (adjust based on system)
if os.name == 'nt':  # Windows
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def extract_text_with_ocr(file_path: str) -> str:
    """
    Extract text from scanned PDF using OCR
    
    Args:
        file_path: Path to PDF file
        
    Returns:
        Extracted text as string
    """
    try:
        logger.info("Starting OCR extraction...")
        
        # Convert PDF to images
        images = convert_from_path(
            file_path,
            dpi=300,  # Higher DPI = better quality
            first_page=1,
            last_page=3  # Only process first 3 pages for performance
        )
        
        logger.info(f"Converted to {len(images)} images")
        
        # OCR each image
        text = ""
        for i, image in enumerate(images):
            # Preprocess image for better OCR
            image = preprocess_image(image)
            
            page_text = pytesseract.image_to_string(
                image,
                lang='eng',
                config='--psm 6'  # Assume uniform block of text
            )
            text += page_text + "\n"
            logger.debug(f"OCR Page {i + 1}: {len(page_text)} chars")
        
        return text.strip()
        
    except Exception as e:
        logger.error(f"OCR failed: {e}")
        return ""


def preprocess_image(image: Image.Image) -> Image.Image:
    """
    Preprocess image for better OCR accuracy
    - Convert to grayscale
    - Increase contrast
    """
    # Convert to grayscale
    image = image.convert('L')
    
    # Enhance contrast
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2.0)
    
    return image