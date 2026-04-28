import sys
from ocr_utils import extract_text_from_image
from ocr_cleaner import clean_extracted_text
from save_to_mongo import save_to_mongodb

def process_receipt(image_path):
    # Step 1: Extract text from the image
    raw_text = extract_text_from_image(image_path)
    print("\nExtracted Text:\n", raw_text)

    # Step 2: Clean the extracted text
    cleaned_data = clean_extracted_text(raw_text)
    print("\nCleaned Data:\n", cleaned_data)

    # Step 3: Save cleaned data to MongoDB
    save_to_mongodb(cleaned_data)
    print("\n✅ Data saved to MongoDB successfully.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("❌ Usage: python process_receipt.py <image_path>")
        sys.exit(1)

    image_path = sys.argv[1]
    process_receipt(image_path)
