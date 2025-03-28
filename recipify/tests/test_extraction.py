import pytest
from datetime import datetime

from recipify.extraction import (
    ReceiptItem,
    ReceiptData,
    WalmartReceiptParser,
    CafeteriaReceiptParser,
    parse_receipt_data,
    ReceiptParsingError,
)

@pytest.fixture
def walmart_receipt_text():
    return """
    Walmart
    123 Main St
    City, State 12345
    
    Apple          1.99
    Banana         0.99
    Milk           3.49
    
    TOTAL         6.47
    
    03/15/24
    14:30
    """

@pytest.fixture
def cafeteria_receipt_text():
    return """
    Campus Cafeteria
    Order Type: Dine-in
    OrderStatus: Completed
    
    Burger 2 X 8.99
    Fries 1 X 2.99
    Soda 1 X 1.99
    
    Total (INR) = 22.96
    
    03/15/24
    12:30
    """

def test_receipt_item_validation():
    # Test valid item
    item = ReceiptItem(name="Test Item", price=9.99)
    assert item.name == "Test Item"
    assert item.price == 9.99
    assert item.quantity == 1
    
    # Test price validation
    with pytest.raises(ValueError):
        ReceiptItem(name="Test Item", price=20000)
    
    # Test empty name validation
    with pytest.raises(ValueError):
        ReceiptItem(name="", price=9.99)

def test_walmart_receipt_parsing(walmart_receipt_text):
    parser = WalmartReceiptParser(walmart_receipt_text)
    result = parser.parse()
    
    assert isinstance(result, ReceiptData)
    assert result.vendor == "Walmart"
    assert result.total == 6.47
    assert len(result.items) == 3
    assert result.date == datetime(2024, 3, 15)
    assert result.time == "14:30"

def test_cafeteria_receipt_parsing(cafeteria_receipt_text):
    parser = CafeteriaReceiptParser(cafeteria_receipt_text)
    result = parser.parse()
    
    assert isinstance(result, ReceiptData)
    assert result.vendor == "Cafeteria"
    assert result.total == 22.96
    assert len(result.items) == 3
    assert result.items[0].quantity == 2
    assert result.metadata["order_type"] == "Dine-in"
    assert result.metadata["order_status"] == "Completed"

def test_empty_receipt():
    with pytest.raises(ValueError):
        parse_receipt_data("")

def test_invalid_receipt():
    result = parse_receipt_data("Invalid receipt text")
    assert "error" in result

def test_receipt_total_validation():
    invalid_receipt = """
    Walmart
    Invalid Total
    """
    result = parse_receipt_data(invalid_receipt)
    assert result["total"] == 0.0 