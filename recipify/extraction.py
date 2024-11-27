import re

def parse_receipt_data(text):
    """
    Extracts key information (amount, date, vendor, and other details) from the receipt text.

    Args:
        text: The extracted text from the receipt.

    Returns:
        A dictionary containing the extracted information.
    """
    data = {}

    try:
        # Extract total amount (handle both "INR" and "INK")
        total_amount_match = re.search(r"Total\s*\(IN[RK]\)\s*=\s*([\d.]+)", text, re.IGNORECASE)
        if total_amount_match:
            data["total"] = float(total_amount_match.group(1))

        # Extract date
        date_match = re.search(r"\d{2}-\d{2}-\d{4}", text)
        if date_match:
            data["date"] = date_match.group(0)

        # Extract time
        time_match = re.search(r"\d{2}:\d{2}", text)
        if time_match:
            data["time"] = time_match.group(0)

        # Extract vendor name (e.g., Cafeteria : Neeram Hall)
        vendor_match = re.search(r"Cafeteria\s*:\s*(.*)", text, re.IGNORECASE)
        if vendor_match:
            data["vendor"] = vendor_match.group(1).strip()

        # Extract order type (e.g., Dine In)
        order_type_match = re.search(r"Order Type:\s*(.*)", text, re.IGNORECASE)
        if order_type_match:
            data["order_type"] = order_type_match.group(1).strip()

        # Extract order status (e.g., Delivered)
        order_status_match = re.search(r"OrderStatus:\s*(.*)", text, re.IGNORECASE)
        if order_status_match:
            data["order_status"] = order_status_match.group(1).strip()

        # Extract items and their quantities/prices (e.g., Tea 2 X 11.42)
        items = re.findall(r"(\w+)\s+(\d+)\s+X\s+([\d.]+)", text)
        if items:
            data["items"] = [{"name": item[0], "quantity": int(item[1]), "price": float(item[2])} for item in items]

    except Exception as e:
        print(f"Error parsing receipt data: {e}")

    return data
