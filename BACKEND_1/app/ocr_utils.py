import os
import pytesseract
from PIL import Image

# ---------------------------------------------------
# Tesseract OCR Configuration
# ---------------------------------------------------

# Change this path only if you move Tesseract later.
pytesseract.pytesseract.tesseract_cmd = r"D:\Software\Tesseract-OCR\tesseract.exe"

print("Using Tesseract from:", pytesseract.pytesseract.tesseract_cmd)


def extract_text_from_image(image_path):
    """
    Extract text from an image using Tesseract OCR.
    """

    try:
        img = Image.open(image_path)

        # Perform OCR
        text = pytesseract.image_to_string(img)

        return text

    except pytesseract.TesseractNotFoundError:
        raise Exception(
            "Tesseract OCR not found. Check the installation path."
        )

    except Exception as e:
        raise Exception(f"OCR Error: {e}")


# ---------------------------------------------------
# Standalone Test
# ---------------------------------------------------

if __name__ == "__main__":

    test_image = "test_receipt.png"

    if os.path.exists(test_image):

        print("\nRunning OCR Test...\n")

        result = extract_text_from_image(test_image)

        print(result)

    else:
        print("Test image not found.")