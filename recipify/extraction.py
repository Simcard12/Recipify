import re
import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime

from pydantic import BaseModel, Field, validator

from recipify.config.settings import settings, patterns
from recipify.utils.logging import setup_logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Compile regex patterns once
PATTERNS = {
    'total': re.compile(r"TOTAL\s*[:\-]?\s*\$?([\d.]+)", re.IGNORECASE),
    'date': re.compile(r"\d{2}/\d{2}/\d{2}"),
    'time': re.compile(r"\d{2}:\d{2}"),
    'items': re.compile(r"([A-Za-z0-9 ]+)\s+([\d.]+)")
}

class ReceiptItem(BaseModel):
    """Model for receipt items with validation."""
    name: str = Field(..., min_length=1)
    price: float = Field(..., gt=0)
    quantity: int = Field(default=1, gt=0)
    
    @validator('price')
    def validate_price(cls, v: float) -> float:
        """Validate price is reasonable."""
        if v > 10000:  # Arbitrary high limit
            raise ValueError(f"Price {v} seems unreasonably high")
        return round(v, 2)

class ReceiptData(BaseModel):
    """Model for receipt data with validation."""
    vendor: str
    total: float
    date: Optional[datetime] = None
    time: Optional[str] = None
    items: List[ReceiptItem] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class ReceiptParsingError(Exception):
    """Custom exception for receipt parsing errors."""
    pass

class BaseReceiptParser(ABC):
    """Abstract base class for receipt parsers."""
    
    def __init__(self, text: str):
        """Initialize parser with receipt text."""
        self.text = text.strip()
        self.data = ReceiptData(
            vendor="Unknown",
            total=0.0,
            items=[],
        )
    
    @abstractmethod
    def parse(self) -> ReceiptData:
        """Parse the receipt text and return structured data."""
        pass
    
    def _extract_total(self) -> Optional[float]:
        """Extract total amount from receipt text."""
        match = patterns.TOTAL.search(self.text)
        if match:
            try:
                return float(match.group(1))
            except ValueError as e:
                logger.warning(f"Failed to convert total amount: {e}")
        return None
    
    def _extract_datetime(self) -> None:
        """Extract date and time from receipt text."""
        date_match = patterns.DATE.search(self.text)
        time_match = patterns.TIME.search(self.text)
        
        if date_match:
            try:
                self.data.date = datetime.strptime(date_match.group(0), "%m/%d/%y")
            except ValueError as e:
                logger.warning(f"Failed to parse date: {e}")
        
        if time_match:
            self.data.time = time_match.group(0)

class WalmartReceiptParser(BaseReceiptParser):
    """Parser for Walmart receipts."""
    
    def parse(self) -> ReceiptData:
        """Parse Walmart receipt format."""
        try:
            self.data.vendor = "Walmart"
            
            # Extract total
            total = self._extract_total()
            if total is not None:
                self.data.total = total
            else:
                logger.warning("Could not extract total amount from Walmart receipt")
            
            # Extract date and time
            self._extract_datetime()
            
            # Extract items
            items = patterns.ITEMS.findall(self.text)
            if items:
                self.data.items = [
                    ReceiptItem(
                        name=item[0].strip(),
                        price=float(item[1])
                    )
                    for item in items
                ]
            
            return self.data
            
        except Exception as e:
            logger.error(f"Error parsing Walmart receipt: {e}")
            raise ReceiptParsingError(f"Failed to parse Walmart receipt: {e}")

class CafeteriaReceiptParser(BaseReceiptParser):
    """Parser for cafeteria receipts."""
    
    def parse(self) -> ReceiptData:
        """Parse cafeteria receipt format."""
        try:
            self.data.vendor = "Cafeteria"
            
            # Extract total with INR/INK handling
            total_match = re.search(r"Total\s*\(IN[RK]\)\s*=\s*([\d.]+)", self.text, re.IGNORECASE)
            if total_match:
                self.data.total = float(total_match.group(1))
            
            # Extract date and time
            self._extract_datetime()
            
            # Extract items with quantity
            items = patterns.QUANTITY.findall(self.text)
            if items:
                self.data.items = [
                    ReceiptItem(
                        name=item[0],
                        quantity=int(item[1]),
                        price=float(item[2])
                    )
                    for item in items
                ]
            
            # Extract metadata
            for field in ["order_type", "order_status"]:
                match = re.search(f"{field}:\s*(.*)", self.text, re.IGNORECASE)
                if match:
                    self.data.metadata[field] = match.group(1).strip()
            
            return self.data
            
        except Exception as e:
            logger.error(f"Error parsing cafeteria receipt: {e}")
            raise ReceiptParsingError(f"Failed to parse cafeteria receipt: {e}")

def classify_receipt(text):
    """
    Classifies the receipt type based on the OCR-extracted text.

    Args:
        text (str): The OCR-extracted text from the receipt.

    Returns:
        str: The type of the receipt ("Walmart", "Cafeteria", "Trader Joe's", or "Unknown").
    """
    try:
        # Check for keywords unique to Walmart receipts
        if re.search(r"\bWalmart\b", text, re.IGNORECASE):
            return "Walmart"

        # Check for keywords unique to Cafeteria receipts
        if re.search(r"\bCafeteria\b", text, re.IGNORECASE):
            return "Cafeteria"

        # Check for Trader Joe's receipts
        if re.search(r"\bTrader Joe\b", text, re.IGNORECASE):
            return "Trader Joe's"

        # Default to "Unknown" if no keywords match
        return "Unknown"

    except Exception as e:
        raise RuntimeError(f"Error classifying receipt: {e}")

def get_receipt_parser(text: str) -> BaseReceiptParser:
    """Factory function to get appropriate receipt parser."""
    text_lower = text.lower()
    
    if "walmart" in text_lower:
        return WalmartReceiptParser(text)
    elif "cafeteria" in text_lower:
        return CafeteriaReceiptParser(text)
    else:
        logger.warning("Unknown receipt type, using default parser")
        return BaseReceiptParser(text)

def parse_receipt_data(text: str) -> Dict[str, Any]:
    """
    Main function to parse receipt data.
    
    Args:
        text: OCR-extracted text from receipt image
        
    Returns:
        Parsed receipt data as dictionary
        
    Raises:
        ReceiptParsingError: If parsing fails
    """
    try:
        if not text.strip():
            raise ValueError("Empty receipt text")
            
        parser = get_receipt_parser(text)
        receipt_data = parser.parse()
        
        # Validate parsed data
        if receipt_data.total <= 0:
            logger.warning("Receipt total is zero or negative")
        if not receipt_data.items:
            logger.warning("No items found in receipt")
            
        return receipt_data.dict()
        
    except Exception as e:
        logger.error(f"Failed to parse receipt: {e}")
        return {"error": str(e)}

def parse_walmart_receipt(text):
    """
    Extracts key information from Walmart receipts.

    Args:
        text (str): The OCR-extracted text from the Walmart receipt.

    Returns:
        dict: Parsed receipt data.
    """
    data = {}
    try:
        # Extract vendor
        data["vendor"] = "Walmart"

        # Extract total amount
        total_match = re.search(r"TOTAL\s*[:\-]?\s*\$?([\d.]+)", text, re.IGNORECASE)
        if total_match:
            data["total"] = float(total_match.group(1))
        else:
            print("WARNING: Could not extract total amount.")
        # Extract date (e.g., MM/DD/YY)
        date_match = re.search(r"\d{2}/\d{2}/\d{2}", text)
        if date_match:
            data["date"] = date_match.group(0)

        # Extract time (e.g., HH:MM)
        time_match = re.search(r"\d{2}:\d{2}", text)
        if time_match:
            data["time"] = time_match.group(0)

        # Extract items
        items = re.findall(r"([A-Za-z0-9 ]+)\s+([\d.]+)", text)
        if items:
            data["items"] = [{"name": item[0].strip(), "price": float(item[1])} for item in items]

    except Exception as e:
        data["error"] = f"Error parsing Walmart receipt: {e}"

    return data

def parse_cafeteria_receipt(text):
    """
    Extracts key information from cafeteria-style receipts.

    Args:
        text (str): The OCR-extracted text from the cafeteria receipt.

    Returns:
        dict: Parsed receipt data.
    """
    data = {}
    try:
        # Extract total amount (handle both "INR" and "INK")
        total_match = re.search(r"Total\s*\(IN[RK]\)\s*=\s*([\d.]+)", text, re.IGNORECASE)
        if total_match:
            data["total"] = float(total_match.group(1))

        # Extract date (e.g., DD-MM-YYYY)
        date_match = re.search(r"\d{2}-\d{2}-\d{4}", text)
        if date_match:
            data["date"] = date_match.group(0)

        # Extract time (e.g., HH:MM)
        time_match = re.search(r"\d{2}:\d{2}", text)
        if time_match:
            data["time"] = time_match.group(0)

        # Extract vendor
        vendor_match = re.search(r"Cafeteria\s*[:\-]?\s*(.*)", text, re.IGNORECASE)
        if vendor_match:
            data["vendor"] = vendor_match.group(1).strip()

        # Extract order type
        order_type_match = re.search(r"Order Type:\s*(.*)", text, re.IGNORECASE)
        if order_type_match:
            data["order_type"] = order_type_match.group(1).strip()

        # Extract order status
        order_status_match = re.search(r"OrderStatus:\s*(.*)", text, re.IGNORECASE)
        if order_status_match:
            data["order_status"] = order_status_match.group(1).strip()

        # Extract items
        items = re.findall(r"(\w+)\s+(\d+)\s+X\s+([\d.]+)", text)
        if items:
            data["items"] = [{"name": item[0], "quantity": int(item[1]), "price": float(item[2])} for item in items]

    except Exception as e:
        data["error"] = f"Error parsing cafeteria receipt: {e}"

    return data

def parse_trader_joes_receipt(text):
    """
    Extracts key information from Trader Joe's receipts.

    Args:
        text (str): The OCR-extracted text from the Trader Joe's receipt.

    Returns:
        dict: Parsed receipt data.
    """
    data = {}
    try:
        # Extract vendor
        data["vendor"] = "Trader Joe's"

        # Extract total amount
        total_match = re.search(r"TOTAL\s*[:\-]?\s*\$?([\d.]+)", text, re.IGNORECASE)
        if total_match:
            data["total"] = float(total_match.group(1))
        else:
            print("WARNING: Could not extract total amount.")
        
        # Extract date (e.g., MM/DD/YY)
        date_match = re.search(r"\d{2}/\d{2}/\d{2}", text)
        if date_match:
            data["date"] = date_match.group(0)

        # Extract time (e.g., HH:MM)
        time_match = re.search(r"\d{2}:\d{2}", text)
        if time_match:
            data["time"] = time_match.group(0)

        # Extract items (simplified pattern for Trader Joe's)
        items = re.findall(r"([A-Za-z0-9 ]+)\s+([\d.]+)", text)
        if items:
            data["items"] = [{"name": item[0].strip(), "price": float(item[1])} for item in items]

    except Exception as e:
        data["error"] = f"Error parsing Trader Joe's receipt: {e}"

    return data
