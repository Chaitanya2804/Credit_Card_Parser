"""
Input validation utilities
"""
from pathlib import Path
from typing import Optional


def validate_pdf_file(filename: str) -> bool:
    """
    Validate if file is a PDF
    
    Args:
        filename: Name of the file
        
    Returns:
        True if valid PDF, False otherwise
    """
    return filename.lower().endswith('.pdf')


def validate_file_size(file_size: int, max_size_mb: int = 10) -> bool:
    """
    Validate file size
    
    Args:
        file_size: Size of file in bytes
        max_size_mb: Maximum allowed size in MB
        
    Returns:
        True if within limit, False otherwise
    """
    max_size_bytes = max_size_mb * 1024 * 1024
    return file_size <= max_size_bytes


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename to prevent path traversal attacks
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    # Remove path components
    filename = Path(filename).name
    
    # Remove dangerous characters
    dangerous_chars = ['..', '/', '\\', ':', '*', '?', '"', '<', '>', '|']
    for char in dangerous_chars:
        filename = filename.replace(char, '_')
    
    return filename