import re

def clean_extracted_text(text):
    """
    Cleans the raw OCR text and extracts structured data like:
    - Vendor Name
    - Date
    - Total Amount
    - List of Items
    """
    lines = text.split('\n')
    lines = [line.strip() for line in lines if line.strip() != '']

    cleaned_data = {
        "vendor": None,
        "date": None,
        "total": None,
        "items": []
    }

    # Try to extract vendor (first line)
    if lines:
        cleaned_data["vendor"] = lines[0]

    # Look for date
    for line in lines:
        match = re.search(r'(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})', line)
        if match:
            cleaned_data["date"] = match.group(1)
            break

    # Look for total
    for line in reversed(lines):
        if 'total' in line.lower():
            match = re.search(r'(\d+\.\d{2})', line)
            if match:
                cleaned_data["total"] = float(match.group(1))
                break

    # Extract items (simplified)
    for line in lines[1:]:
        if re.search(r'[a-zA-Z]+\s+\d+\.\d{2}', line):
            cleaned_data["items"].append(line)

    return cleaned_data
