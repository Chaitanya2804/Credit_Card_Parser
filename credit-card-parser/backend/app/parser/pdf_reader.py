"""
Extract text from PDF files using PyPDF2
"""
import PyPDF2
import logging

logger = logging.getLogger(__name__)


def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract text from PDF using PyPDF2 (for digital PDFs)
    
    Args:
        file_path: Path to PDF file
        
    Returns:
        Extracted text as string
    """
    try:
        text = ""
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            logger.info(f"PDF has {len(pdf_reader.pages)} pages")
            
            for page_num, page in enumerate(pdf_reader.pages):
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
                    logger.debug(f"Page {page_num + 1}: {len(page_text)} chars")
        
        return text.strip()
        
    except Exception as e:
        logger.error(f"Error reading PDF: {e}")
        return ""