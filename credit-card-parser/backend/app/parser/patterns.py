"""
Regex patterns organized by issuer (optional enhancement)
"""

# Future enhancement: Store issuer-specific patterns here
HDFC_PATTERNS = {
    "card_number": r"Card\s+Number[:\s]+X+(\d{4})",
    "amount": r"Total\s+Amount\s+Due[:\s]+₹\s*([\d,]+\.?\d*)"
}
SBI_PATTERNS = {
"card_number": r"Card\s+No.[:\s]+*+(\d{4})",
"amount": r"Amount\s+Payable[:\s]+Rs.\s*([\d,]+.?\d*)"
}
ICICI_PATTERNS = {
"card_number": r"Card\s+ending\s+in[:\s]+(\d{4})",
"amount": r"Total\s+Due[:\s]+INR\s*([\d,]+.?\d*)"
}
AXIS_PATTERNS = {
"card_number": r"Card\s+Number[:\s]+XXXX-XXXX-XXXX-(\d{4})",
"amount": r"Outstanding\s+Amount[:\s]+₹\s*([\d,]+.?\d*)"
}
KOTAK_PATTERNS = {
"card_number": r"Card\s+Last\s+4\s+Digits[:\s]+(\d{4})",
"amount": r"Payment\s+Due[:\s]+Rs\s*([\d,]+.?\d*)"
}

ISSUER_PATTERNS_MAP = {
"HDFC Bank": HDFC_PATTERNS,
"SBI Card": SBI_PATTERNS,
"ICICI Bank": ICICI_PATTERNS,
"Axis Bank": AXIS_PATTERNS,
"Kotak Mahindra": KOTAK_PATTERNS
}