import re
import json

def parse_receipt(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    
    date_time_match = re.search(r'(\d{2}\.\d{2}\.\d{4})\s+(\d{2}:\d{2}:\d{2})', content)
    date = date_time_match.group(1) if date_time_match else None
    time = date_time_match.group(2) if date_time_match else None

    
    payment_method_match = re.search(r'([А-Яа-я\s]+):\s+[\d\s,.]+\nИТОГО:', content)
    payment_method = payment_method_match.group(1).strip() if payment_method_match else "Unknown"

    
    products = []
    product_pattern = re.compile(
        r'\d+\.\n(.*?)\n([\d\s,]+)\s*x\s*([\d\s,.]+)\n([\d\s,.]+)', 
        re.DOTALL
    )
    
    matches = product_pattern.findall(content)
    
    for match in matches:
        name = match[0].replace('\n', ' ').strip()
        
        quantity = float(match[1].replace(' ', '').replace(',', '.'))
        price_per_unit = float(match[2].replace(' ', '').replace(',', '.'))
        subtotal = float(match[3].replace(' ', '').replace(',', '.'))
        
        products.append({
            "name": name,
            "quantity": quantity,
            "price_per_unit": price_per_unit,
            "subtotal": subtotal
        })

    
    calculated_total = sum(item['subtotal'] for item in products)
    
    
    receipt_total_match = re.search(r'ИТОГО:\s+([\d\s,.]+)', content)
    receipt_total = float(receipt_total_match.group(1).replace(' ', '').replace(',', '.')) if receipt_total_match else 0.0

    
    return {
        "metadata": {
            "date": date,
            "time": time,
            "payment_method": payment_method,
            "location": "Nur-Sultan, Kazakhstan"
        },
        "items": products,
        "financials": {
            "calculated_total": calculated_total,
            "receipt_total": receipt_total,
            "currency": "KZT"
        }
    }

if __name__ == "__main__":
    try:
        data = parse_receipt('raw.txt')
        print(json.dumps(data, indent=4, ensure_ascii=False))
    except FileNotFoundError:
        print("Error: raw.txt not found. Please ensure the file is in the same directory.")