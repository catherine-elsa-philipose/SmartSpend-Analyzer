from ocr_utils import extract_text_from_image 
from ocr_cleaner import clean_ocr_text 
 
image_path = "C:/Users/DELL/Desktop/SmartSpend/BACKEND_1/test_receipts/final.jpg" 
ocr_text = extract_text_from_image(image_path) 
 
print("\n--- OCR Extracted Text ---\n") 
print(ocr_text) 
 
cleaned_data = clean_ocr_text(ocr_text) 
print("\n--- Cleaned Data ---\n") 
print(cleaned_data) 
