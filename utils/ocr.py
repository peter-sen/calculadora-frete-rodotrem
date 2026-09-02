import pytesseract
from PIL import Image
import io
import re

def extract_mileage(image_bytes):
    """
    Extracts the mileage from a Google Maps screenshot using OCR.
    Assumes the text contains something like '1.234 km' or '123 km'.
    """
    try:
        image = Image.open(io.BytesIO(image_bytes))

        # We assume the user might provide an image in Portuguese, so 'por' is specified.
        # It's good to use 'por+eng' to capture standard characters and numbers accurately.
        text = pytesseract.image_to_string(image, lang='por+eng')

        # Look for numbers followed by 'km' (case insensitive).
        # Supports numbers with dot or comma as thousands/decimal separator.
        matches = re.findall(r'(\d+[.,\s]?\d*)\s*km', text, re.IGNORECASE)

        if matches:
            # We take the largest number found assuming it's the total trip distance,
            # though usually there's only one main distance.
            # Convert to a standard float format.
            distances = []
            for match in matches:
                # Remove spaces, replace comma with dot. For thousands separator (e.g. 1.234),
                # we need to be careful. In Brazil, dot is thousand separator and comma is decimal.
                # Since distances in long trips are often > 1000, 1.234 km means 1234 km.
                # Let's strip dots if there are no commas, or handle it robustly.

                clean_match = match.replace(' ', '')
                if ',' in clean_match:
                    clean_match = clean_match.replace('.', '').replace(',', '.')
                else:
                    # If there's a dot but no comma, in PT-BR it's usually a thousand separator.
                    # e.g., 1.234 km -> 1234
                    clean_match = clean_match.replace('.', '')

                distances.append(float(clean_match))

            if distances:
                return max(distances)
        return None
    except Exception as e:
        print(f"Error in OCR: {e}")
        return None
