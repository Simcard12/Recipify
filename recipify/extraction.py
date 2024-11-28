import re

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

def parse_receipt_data(text):
    """
    Classifies the receipt and extracts information using the appropriate parsing logic.

    Args:
        text (str): The OCR-extracted text from the receipt.

    Returns:
        dict: The parsed receipt data or an error message.
    """
    try:
        # Classify the receipt
        receipt_type = classify_receipt(text)
        print(f"Classified Receipt Type: {receipt_type}")

        # Parse based on receipt type
        if receipt_type == "Walmart":
            return parse_walmart_receipt(text)
        elif receipt_type == "Cafeteria":
            return parse_cafeteria_receipt(text)
        elif receipt_type == "Trader Joe's":
            return parse_trader_joes_receipt(text)
        else:
            return {"error": "Unknown receipt format"}
    except Exception as e:
        return {"error": f"Failed to parse receipt: {e}"}

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
