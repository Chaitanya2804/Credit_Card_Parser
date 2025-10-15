"""
Unit tests for parser functionality
Run with: pytest tests/test_parser.py -v
"""
import pytest
from app.parser.issuer_detector import detect_issuer
from app.parser.extractors import (
    extract_card_last_four,
    extract_billing_cycle,
    extract_due_date,
    extract_total_amount_due,
    extract_fields
)


class TestIssuerDetection:
    """Test issuer detection logic"""
    
    def test_hdfc_detection(self):
        text = "HDFC Bank Credit Card Statement"
        assert detect_issuer(text) == "HDFC Bank"
    
    def test_sbi_detection(self):
        text = "SBI Card Payment Details"
        assert detect_issuer(text) == "SBI Card"
    
    def test_icici_detection(self):
        text = "ICICI Bank Credit Card Monthly Statement"
        assert detect_issuer(text) == "ICICI Bank"
    
    def test_axis_detection(self):
        text = "Axis Bank Statement Period"
        assert detect_issuer(text) == "Axis Bank"
    
    def test_kotak_detection(self):
        text = "Kotak Mahindra Bank Card Statement"
        assert detect_issuer(text) == "Kotak Mahindra"
    
    def test_unknown_issuer(self):
        text = "Some Random Bank Statement"
        assert detect_issuer(text) == "Unknown"


class TestCardExtraction:
    """Test card last 4 digits extraction"""
    
    def test_extract_with_x_format(self):
        text = "Card Number: XXXX XXXX XXXX 1234"
        result = extract_card_last_four(text, "HDFC Bank")
        assert result["value"] == "1234"
        assert result["confidence"] > 0.8
    
    def test_extract_with_asterisk(self):
        text = "Card ending in: ****1234"
        result = extract_card_last_four(text, "SBI Card")
        assert result["value"] == "1234"
    
    def test_extract_not_found(self):
        text = "No card number here"
        result = extract_card_last_four(text, "ICICI Bank")
        assert result["value"] is None
        assert result["confidence"] == 0.0


class TestBillingCycleExtraction:
    """Test billing cycle extraction"""
    
    def test_extract_date_range(self):
        text = "Statement Period: 01/01/2024 to 31/01/2024"
        result = extract_billing_cycle(text, "HDFC Bank")
        assert "01/01/2024" in result["value"]
        assert "31/01/2024" in result["value"]
        assert result["confidence"] > 0.8
    
    def test_extract_month_format(self):
        text = "Billing Cycle: 1 January 2024 to 31 January 2024"
        result = extract_billing_cycle(text, "Axis Bank")
        assert result["value"] is not None
    
    def test_extract_not_found(self):
        text = "No billing cycle information"
        result = extract_billing_cycle(text, "ICICI Bank")
        assert result["value"] is None


class TestDueDateExtraction:
    """Test payment due date extraction"""
    
    def test_extract_due_date(self):
        text = "Payment Due Date: 15/02/2024"
        result = extract_due_date(text, "HDFC Bank")
        assert result["value"] == "15/02/2024"
        assert result["confidence"] > 0.8
    
    def test_extract_pay_by(self):
        text = "Pay by: 20-02-2024"
        result = extract_due_date(text, "SBI Card")
        assert "20" in result["value"]
        assert "02" in result["value"]
    
    def test_extract_not_found(self):
        text = "No due date mentioned"
        result = extract_due_date(text, "Kotak Mahindra")
        assert result["value"] is None


class TestAmountExtraction:
    """Test total amount due extraction"""
    
    def test_extract_with_rupee_symbol(self):
        text = "Total Amount Due: ₹15,234.50"
        result = extract_total_amount_due(text, "HDFC Bank")
        assert "15234.50" in result["value"]
        assert result["confidence"] > 0.8
    
    def test_extract_with_rs(self):
        text = "Amount Payable: Rs. 5,000"
        result = extract_total_amount_due(text, "ICICI Bank")
        assert "5000" in result["value"]
    
    def test_extract_plain_number(self):
        text = "Outstanding Balance: 12500.00"
        result = extract_total_amount_due(text, "Axis Bank")
        assert "12500" in result["value"]
    
    def test_extract_not_found(self):
        text = "No amount information"
        result = extract_total_amount_due(text, "SBI Card")
        assert result["value"] is None


class TestFullExtraction:
    """Test complete field extraction"""
    
    def test_full_statement_extraction(self):
        sample_statement = """
        HDFC Bank Credit Card Statement
        
        Card Number: XXXX XXXX XXXX 5678
        Statement Period: 01/01/2024 to 31/01/2024
        Payment Due Date: 20/02/2024
        Total Amount Due: ₹25,450.00
        
        Please pay by the due date to avoid late fees.
        """
        
        issuer = detect_issuer(sample_statement)
        fields = extract_fields(sample_statement, issuer)
        
        assert fields["issuer"]["value"] == "HDFC Bank"
        assert fields["card_last_four"]["value"] == "5678"
        assert "01/01/2024" in fields["billing_cycle"]["value"]
        assert fields["due_date"]["value"] == "20/02/2024"
        assert "25450" in fields["total_amount_due"]["value"]
        
        # Check all fields have confidence scores
        for field_name, field_data in fields.items():
            assert "confidence" in field_data
            assert "method" in field_data


class TestEdgeCases:
    """Test edge cases and error handling"""
    
    def test_empty_text(self):
        fields = extract_fields("", "Unknown")
        assert all(f["confidence"] == 0.0 for f in fields.values() if f["value"] is None)
    
    def test_malformed_dates(self):
        text = "Due Date: Invalid-Date-Format"
        result = extract_due_date(text, "HDFC Bank")
        # Should not crash, return None
        assert result["value"] is None or result["confidence"] < 0.5
    
    def test_mixed_case_text(self):
        text = "hDfC BaNk CrEdIt CaRd"
        issuer = detect_issuer(text)
        assert issuer == "HDFC Bank"


# Fixtures for mock data
@pytest.fixture
def sample_hdfc_statement():
    return """
    HDFC Bank Credit Card Statement
    Card ending in 4321
    Statement from 01-Jan-2024 to 31-Jan-2024
    Payment due by 20-Feb-2024
    Total outstanding: Rs. 18,750.50
    """


@pytest.fixture
def sample_sbi_statement():
    return """
    SBI Card Monthly Statement
    Card Number: XXXXXXXXXXXX9876
    Billing Period: 15/12/2023 - 14/01/2024
    Due Date: 05/02/2024
    Amount Payable: ₹32,100
    """


def test_with_hdfc_fixture(sample_hdfc_statement):
    """Test with HDFC fixture"""
    issuer = detect_issuer(sample_hdfc_statement)
    fields = extract_fields(sample_hdfc_statement, issuer)
    
    assert issuer == "HDFC Bank"
    assert fields["card_last_four"]["value"] == "4321"
    assert "18750.50" in fields["total_amount_due"]["value"]


def test_with_sbi_fixture(sample_sbi_statement):
    """Test with SBI fixture"""
    issuer = detect_issuer(sample_sbi_statement)
    fields = extract_fields(sample_sbi_statement, issuer)
    
    assert issuer == "SBI Card"
    assert fields["card_last_four"]["value"] == "9876"
    assert "32100" in fields["total_amount_due"]["value"]


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=app.parser"])