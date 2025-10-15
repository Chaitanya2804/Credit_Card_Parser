"""
Detect credit card issuer from statement text
"""
import re
import logging

logger = logging.getLogger(__name__)

# Issuer detection patterns
ISSUER_PATTERNS = {
    "ICICI Bank": [
        r"ICICI\s+Bank",
        r"ICICIBANK",
        r"ICICI\s+Credit\s+Card",
        r"ICICI",  # Simple match for ICICI
        r"iCiCi",  # Case variations
        r"VIEW\s+LAST\s+STATEMENT.*ICICI",  # Specific to ICICI statement format
        r"Card\s+Holder\s+Name.*Statement\s+Date.*Payment\s+Due\s+Date",  # ICICI statement structure
    ],
    "HDFC Bank": [
        r"HDFC\s+Bank",
        r"HDFCBANK",
        r"HDFC\s+Credit\s+Card"
    ],
    "SBI Card": [
        r"SBI\s+Card",
        r"State\s+Bank\s+of\s+India",
        r"SBICARD"
    ],
    "Axis Bank": [
        r"Axis\s+Bank",
        r"AXISBANK",
        r"Axis\s+Credit\s+Card"
    ],
    "Kotak Mahindra": [
        r"kotak",  # Simple match - very important!
        r"Kotak\s+Mahindra",
        r"Kotak\s+Bank",
        r"KOTAKBANK",
        r"My\s+Kotak",
        r"Kotak\s+Credit",
        r"KOTAK\s+MAHINDRA\s+BANK"
    ]
}


def detect_issuer(text: str) -> str:
    """
    Detect credit card issuer from statement text
    
    Args:
        text: Extracted text from PDF
        
    Returns:
        Issuer name or "Unknown"
    """
    # Convert to uppercase for matching
    text_upper = text.upper()
    
    # Check first 1000 characters specifically (where bank name usually appears)
    text_preview = text[:1000].upper()
    
    # Try each issuer
    for issuer, patterns in ISSUER_PATTERNS.items():
        for pattern in patterns:
            # Check both full text and preview
            if re.search(pattern, text_upper, re.IGNORECASE) or re.search(pattern, text_preview, re.IGNORECASE | re.DOTALL):
                logger.info(f"Issuer detected: {issuer} (pattern: {pattern})")
                return issuer
    
    # Log first 500 characters to help debug
    logger.warning(f"Could not detect issuer. Text preview: {text[:500]}")
    return "Unknown"