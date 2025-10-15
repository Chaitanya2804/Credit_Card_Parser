"""
Extract 5 key fields from credit card statements
Supports: Kotak Mahindra, SBI Card, HDFC, ICICI, Axis
"""
import re
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


def extract_fields(text: str, issuer: str) -> Dict[str, Dict[str, Any]]:
    """
    Extract 5 key fields based on issuer
    
    Returns:
        Dictionary with field name as key and {value, confidence, method} as value
    """
    extractors = {
        "card_last_four": extract_card_last_four,
        "billing_cycle": extract_billing_cycle,
        "due_date": extract_due_date,
        "total_amount_due": extract_total_amount_due
    }
    
    results = {
        "issuer": {
            "value": issuer,
            "confidence": 1.0 if issuer != "Unknown" else 0.5,
            "method": "pattern_matching"
        }
    }
    
    for field_name, extractor_func in extractors.items():
        try:
            result = extractor_func(text, issuer)
            results[field_name] = result
            logger.info(f"Extracted {field_name}: {result}")
        except Exception as e:
            logger.error(f"Error extracting {field_name}: {e}", exc_info=True)
            results[field_name] = {
                "value": None,
                "confidence": 0.0,
                "method": "error"
            }
    
    return results


def extract_card_last_four(text: str, issuer: str) -> Dict[str, Any]:
    """Extract last 4 digits of card number"""
    patterns = [
        # Axis format: "Card No: 45145700****5541"
        r"Card\s+No[:\s]+\d+\*+(\d{4})",
        r"Card\s+Number[:\s]+\d+\*+(\d{4})",
        
        # SBI format: "XXXX XXXX XXXX XX86"
        r"X+\s+X+\s+X+\s+X*(\d{2,4})",
        r"Credit\s+Card\s+Number[:\s]+X+\s+X+\s+X+\s+X*(\d{2,4})",
        
        # Kotak format: "4147 XXXX XXXX 1420"
        r"(\d{4})\s+X+\s+X+\s+(\d{4})",
        r"Primary\s+Card\s+Number[:\s]+\d+\s+X+\s+X+\s+(\d{4})",
        r"Card\s+Number[:\s]+\d+\s+X+\s+X+\s+(\d{4})",
        
        # Standard formats
        r"card\s+(?:number|no\.?|#)?\s*[:\-]?\s*X+(\d{4})",
        r"XXXX\s*XXXX\s*XXXX\s*(\d{4})",
        r"(?:ending|last)\s+(?:digits?|4)?\s*[:\-]?\s*(\d{4})",
        r"\*+\s*(\d{4})",
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            last_four = match.group(match.lastindex) if match.lastindex else match.group(1)
            logger.info(f"Card last 4 found: {last_four} using pattern: {pattern}")
            return {
                "value": last_four,
                "confidence": 0.9,
                "method": "regex"
            }
    
    logger.warning("Card last 4 not found")
    return {"value": None, "confidence": 0.0, "method": "not_found"}


def extract_billing_cycle(text: str, issuer: str) -> Dict[str, Any]:
    """Extract billing cycle/statement period"""
    
    # Clean text - normalize whitespace
    clean_text = ' '.join(text.split())
    
    logger.info(f"Searching for billing cycle in text length: {len(clean_text)}")
    
    patterns = [
        # Axis format: "19/10/2019 - 18/11/2019" in table header row
        r"(\d{2}/\d{2}/\d{4})\s*-\s*(\d{2}/\d{2}/\d{4})",
        r"Statement\s+Period\s+(\d{2}/\d{2}/\d{4})\s*-\s*(\d{2}/\d{2}/\d{4})",
        
        # ICICI format: "Statement Period 27-08-2025 TO 26-09-2025"
        r"Statement\s+Period\s+(\d{2}-\d{2}-\d{4})\s+TO\s+(\d{2}-\d{2}-\d{4})",
        r"Billing\s+Period[:\s]+(\d{2}-\d{2}-\d{4})\s+TO\s+(\d{2}-\d{2}-\d{4})",

        # SBI format: "for Statement Period: 03 Aug 25 to 02 Sep 25"
        r"Statement\s+Period[:\s]+(\d{1,2}\s+[A-Za-z]{3}\s+\d{2})\s+to\s+(\d{1,2}\s+[A-Za-z]{3}\s+\d{2})",
        r"for\s+Statement\s+Period[:\s]+(\d{1,2}\s+[A-Za-z]{3}\s+\d{2})\s+to\s+(\d{1,2}\s+[A-Za-z]{3}\s+\d{2})",
        
        # Kotak format: "26-Jul-2025 to 25-Aug-2025"
        r"(\d{1,2}[\s\-][A-Za-z]{3}[\s\-]\d{4})[\s\w]*to[\s\w]*(\d{1,2}[\s\-][A-Za-z]{3}[\s\-]\d{4})",
        r"from\s+(\d{1,2}[\s\-][A-Za-z]{3}[\s\-]\d{4})\s+to\s+(\d{1,2}[\s\-][A-Za-z]{3}[\s\-]\d{4})",
        r"details\s+from\s+(\d{1,2}[\s\-][A-Za-z]{3}[\s\-]\d{4})\s+to\s+(\d{1,2}[\s\-][A-Za-z]{3}[\s\-]\d{4})",
        r"Transaction\s+details\s+from\s+(\d{1,2}[\s\-][A-Za-z]{3}[\s\-]\d{4})\s+to\s+(\d{1,2}[\s\-][A-Za-z]{3}[\s\-]\d{4})",
        
        # Standard formats
        r"(?:billing|statement)\s+(?:period|cycle|date)[:\-\s]+(\d{1,2}[/\-]\d{1,2}[/\-]\d{2,4})\s+to\s+(\d{1,2}[/\-]\d{1,2}[/\-]\d{2,4})",
        r"statement\s+from\s+(\d{1,2}[/\-]\d{1,2}[/\-]\d{2,4})\s+to\s+(\d{1,2}[/\-]\d{1,2}[/\-]\d{2,4})",
        r"(\d{1,2}\s+[A-Za-z]{3,9}\s+\d{4})\s+to\s+(\d{1,2}\s+[A-Za-z]{3,9}\s+\d{4})",
        r"(\d{1,2}-[A-Za-z]{3}-\d{4})\s+to\s+(\d{1,2}-[A-Za-z]{3}-\d{4})",
    ]
    
    for i, pattern in enumerate(patterns):
        match = re.search(pattern, clean_text, re.IGNORECASE)
        if match:
            date1 = match.group(1).strip()
            date2 = match.group(2).strip()
            
            # For non-slash formats, normalize with dashes
            if '/' not in date1:
                date1 = re.sub(r'\s+', '-', date1)
            if '/' not in date2:
                date2 = re.sub(r'\s+', '-', date2)
                
            cycle = f"{date1} to {date2}"
            logger.info(f"Billing cycle found: {cycle} using pattern #{i}")
            return {
                "value": cycle,
                "confidence": 0.85,
                "method": "regex"
            }
    
    logger.warning(f"Billing cycle not found. Text preview: {clean_text[:1000]}")
    
    # Fallback: Look for any two dates near each other
    date_pattern = r"\d{1,2}[-\s][A-Za-z]{3}[-\s]\d{2,4}"
    dates = re.findall(date_pattern, clean_text[:2000])
    if len(dates) >= 2:
        cycle = f"{dates[0]} to {dates[1]}"
        logger.info(f"Billing cycle extracted from nearby dates: {cycle}")
        return {
            "value": cycle,
            "confidence": 0.70,
            "method": "fallback"
        }
    
    return {"value": None, "confidence": 0.0, "method": "not_found"}


def extract_due_date(text: str, issuer: str) -> Dict[str, Any]:
    """Extract payment due date - Ultra flexible version"""
    
    # Clean text
    clean_text = re.sub(r'\s+', ' ', text)
    
    # Log first 2000 chars for debugging
    logger.info(f"Searching for due date in text preview: {clean_text[:2000]}")
    
    # Extract billing cycle dates first to exclude them
    billing_dates = set()
    billing_pattern = r"(\d{2}/\d{2}/\d{4})\s*-\s*(\d{2}/\d{2}/\d{4})"
    billing_match = re.search(billing_pattern, clean_text)
    if billing_match:
        billing_dates.add(billing_match.group(1))
        billing_dates.add(billing_match.group(2))
        logger.info(f"Found billing dates to exclude: {billing_dates}")
    
    # Axis-specific: Look for "Payment Due Date" label and extract date from table structure
    # The table header has: Total Payment Due | Minimum Payment Due | Statement Period | Payment Due Date
    # Pattern looks for the header row with "Payment Due Date" and extracts the last DD/MM/YYYY date in that context
    axis_table_header_pattern = r"Total\s+Payment\s+Due\s+Minimum\s+Payment\s+Due\s+Statement\s+Period\s+Payment\s+Due\s+Date.*?(\d{2}/\d{2}/\d{4})"
    axis_header_match = re.search(axis_table_header_pattern, clean_text, re.IGNORECASE | re.DOTALL)
    if axis_header_match:
        due_date = axis_header_match.group(1).strip()
        if due_date not in billing_dates:
            logger.info(f"Due date found (Axis table header with context): {due_date}")
            return {
                "value": due_date,
                "confidence": 0.95,
                "method": "regex"
            }
    
    # Alternative Axis approach: Find dates in the PAYMENT SUMMARY section only (first 1000 chars)
    # This avoids transaction dates which appear later
    axis_date_pattern = r"\d{2}/\d{2}/\d{4}"
    all_axis_dates = re.findall(axis_date_pattern, clean_text[:1000])  # Reduced from 1500 to 1000
    
    if all_axis_dates and len(billing_dates) > 0:
        logger.info(f"Found all Axis dates in first 1000 chars: {all_axis_dates}")
        # Filter out billing dates
        potential_due_dates = [date for date in all_axis_dates if date not in billing_dates]
        logger.info(f"Potential due dates after filtering: {potential_due_dates}")
        
        # Take the LAST date (payment due date appears after billing dates in the table)
        if potential_due_dates:
            due_date = potential_due_dates[-1]  # Changed from [0] to [-1] to get the last date
            logger.info(f"Due date found (Axis dates filter - last date): {due_date}")
            return {
                "value": due_date,
                "confidence": 0.90,
                "method": "regex"
            }
    
    # ICICI-specific: Look for "Payment Due Date DD-MM-YYYY" format
    icici_pattern = r"Payment\s+Due\s+Date\s+(\d{2}-\d{2}-\d{4})"
    icici_match = re.search(icici_pattern, clean_text, re.IGNORECASE)
    if icici_match:
        due_date = icici_match.group(1).strip()
        logger.info(f"Due date found (ICICI specific): {due_date}")
        return {
            "value": due_date,
            "confidence": 0.95,
            "method": "regex"
        }
    
    patterns = [
        # Axis patterns with DD/MM/YYYY format
        r"Payment\s+Due\s+Date[:\s]*(\d{2}/\d{2}/\d{4})",
        r"Due\s+Date[:\s]*(\d{2}/\d{2}/\d{4})",
        
        # ICICI patterns with DD-MM-YYYY format
        r"Payment\s+Due\s+Date[:\s]*(\d{2}-\d{2}-\d{4})",
        r"Due\s+Date[:\s]*(\d{2}-\d{2}-\d{4})",
        
        # Ultra flexible - just find "22 Sep 2025" anywhere near "due" or "payment"
        r"(?:payment|due|pay).*?(\d{1,2}\s+[A-Za-z]{3}\s+\d{4})",
        r"(\d{1,2}\s+[A-Za-z]{3}\s+\d{4}).*?(?:payment|due|pay)",
        
        # SBI specific patterns
        r"Payment\s+Due\s+Date[:\s]*(\d{1,2}\s+[A-Za-z]{3}\s+\d{4})",
        r"Due\s+Date[:\s]*(\d{1,2}\s+[A-Za-z]{3}\s+\d{4})",
        r"Pay\s+(?:by|before)[:\s]*(\d{1,2}\s+[A-Za-z]{3}\s+\d{4})",
        
        # Kotak format
        r"pay\s+by\s+(\d{1,2}-[A-Za-z]{3}-\d{4})",
        r"Remember\s+to\s+pay\s+by\s+(\d{1,2}-[A-Za-z]{3}-\d{4})",
        r"by\s+(\d{1,2}-[A-Za-z]{3}-\d{4})",
        
        # More flexible
        r"Due[:\s]+(\d{1,2}\s+[A-Za-z]{3}\s+\d{4})",
        r"Due[:\s]+(\d{1,2}-[A-Za-z]{3}-\d{4})",
        
        # Standard formats
        r"(?:payment\s+)?due\s+(?:date|by)[:\-\s]+(\d{1,2}[/\-]\d{1,2}[/\-]\d{2,4})",
        r"pay\s+by[:\-\s]+(\d{1,2}[/\-]\d{1,2}[/\-]\d{2,4})",
        r"due\s+on[:\-\s]+(\d{1,2}\s+[A-Za-z]{3,9}\s+\d{4})",
    ]
    
    for pattern in patterns:
        match = re.search(pattern, clean_text, re.IGNORECASE)
        if match:
            due_date = match.group(1).strip()
            
            # Skip if it's a billing cycle date
            if due_date in billing_dates:
                logger.info(f"Skipping date {due_date} - it's a billing cycle date")
                continue
                
            logger.info(f"Due date found: {due_date} using pattern: {pattern}")
            return {
                "value": due_date,
                "confidence": 0.9,
                "method": "regex"
            }
    
    # Last resort: Find ANY date in format "DD MMM YYYY" in first 3000 chars
    simple_date = r"\d{1,2}\s+[A-Za-z]{3}\s+\d{4}"
    if re.search(r"(?:due|payment)", clean_text[:3000], re.IGNORECASE):
        # Find all dates
        all_dates = re.findall(simple_date, clean_text[:3000])
        if len(all_dates) >= 2:
            due_date = all_dates[1]
            logger.info(f"Due date found via fallback: {due_date}")
            return {
                "value": due_date,
                "confidence": 0.70,
                "method": "fallback"
            }
    
    logger.warning(f"Due date not found. Text preview: {clean_text[:500]}")
    return {"value": None, "confidence": 0.0, "method": "not_found"}


def extract_total_amount_due(text: str, issuer: str) -> Dict[str, Any]:
    """Extract total amount due - Ultra flexible version"""
    
    # Log for debugging
    logger.info(f"Searching for amount in text preview: {text[:2000]}")
    
    # Axis-specific: Look for "Total Payment Due XXXXX.XX Dr" format
    axis_pattern = r"Total\s+Payment\s+Due\s+([\d,]+\.?\d*)\s+Dr"
    axis_match = re.search(axis_pattern, text, re.IGNORECASE)
    if axis_match:
        amount = axis_match.group(1).replace(',', '').strip()
        try:
            amount_float = float(amount)
            logger.info(f"Total amount found (Axis specific): ₹{amount_float:.2f}")
            return {
                "value": f"₹{amount_float:.2f}",
                "confidence": 0.95,
                "method": "regex"
            }
        except ValueError:
            pass
    
    # ICICI-specific: Look for "Total Amount Due INR XXXXX.XX" format
    icici_pattern = r"Total\s+Amount\s+Due\s+INR\s+([\d,.]+)"
    icici_match = re.search(icici_pattern, text, re.IGNORECASE)
    if icici_match:
        amount = icici_match.group(1).replace(',', '').strip()
        try:
            amount_float = float(amount)
            logger.info(f"Total amount found (ICICI specific): ₹{amount_float:.2f}")
            return {
                "value": f"₹{amount_float:.2f}",
                "confidence": 0.95,
                "method": "regex"
            }
        except ValueError:
            pass
    
    patterns = [
        # Axis patterns
        r"Total\s+Payment\s+Due\s+([\d,]+\.?\d*)\s+Dr",
        r"Total\s+Payment\s+Due[:\s]+([\d,]+\.?\d*)",
        
        # ICICI patterns with INR
        r"Total\s+Amount\s+Due\s+INR\s+([\d,.]+)",
        r"Total\s+Amount\s+Due[:\s]+INR\s+([\d,.]+)",
        
        # Ultra flexible - find any amount near "Total Amount Due"
        r"Total\s+Amount\s+Due.*?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)",
        r"\*\s*Total\s+Amount\s+Due.*?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)",
        
        # SBI specific with symbol
        r"\*Total\s+Amount\s+Due\s*\([₹\$]\)\s*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)",
        r"\*Total\s+Amount\s+Due[:\s]*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)",
        r"Total\s+Amount\s+Due\s*\([₹\$]\)\s*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)",
        r"Total\s+Amount\s+Due[:\s]*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)",
        
        # Kotak format
        r"Total\s+Amount\s+Due\s+\(TAD\)\s+(?:Rs\.?|₹)?\s*([\d,]+\.?\d*)",
        r"Total\s+Amount\s+Due\s+\(Payable\)\s+(?:Rs\.?|₹)?\s*([\d,]+\.?\d*)",
        r"TAD[:\-\s]+(?:Rs\.?|₹)?\s*([\d,]+\.?\d*)",
        
        # Standard with currency
        r"total\s+(?:amount\s+)?due[:\-\s]*(?:Rs\.?|INR|₹)?\s*([\d,]+\.?\d*)",
        r"amount\s+payable[:\-\s]+(?:Rs\.?|INR|₹)?\s*([\d,]+\.?\d*)",
        r"(?:minimum\s+)?payment\s+due[:\-\s]+(?:Rs\.?|INR|₹)?\s*([\d,]+\.?\d*)",
        r"outstanding\s+(?:balance|amount)[:\-\s]+(?:Rs\.?|INR|₹)?\s*([\d,]+\.?\d*)",
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            amount = match.group(1).replace(',', '').strip()
            try:
                amount_float = float(amount)
                logger.info(f"Total amount found: ₹{amount_float:.2f} using pattern: {pattern}")
                return {
                    "value": f"₹{amount_float:.2f}",
                    "confidence": 0.85,
                    "method": "regex"
                }
            except ValueError:
                logger.warning(f"Could not convert amount to float: {amount}")
                continue
    
    # Last resort: Find amount with asterisk and numbers
    fallback_pattern = r"\*.*?(\d{1,3}(?:,\d{3})+(?:\.\d{2})?)"
    match = re.search(fallback_pattern, text[:3000])
    if match:
        amount = match.group(1).replace(',', '').strip()
        try:
            amount_float = float(amount)
            logger.info(f"Total amount found via fallback: ₹{amount_float:.2f}")
            return {
                "value": f"₹{amount_float:.2f}",
                "confidence": 0.70,
                "method": "fallback"
            }
        except ValueError:
            pass
    
    logger.warning("Total amount not found")
    return {"value": None, "confidence": 0.0, "method": "not_found"}