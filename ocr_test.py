import pytesseract
import re
from PIL import Image, ImageEnhance, ImageFilter

# ✅ Set the correct Tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text(image_path):
    """Extracts text from an image using Tesseract OCR with preprocessing."""
    try:
        image = Image.open(image_path)
        image = image.convert("L")  # Convert to grayscale
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(2.0)
        image = image.filter(ImageFilter.EDGE_ENHANCE)
        text = pytesseract.image_to_string(image)
        return text
    except FileNotFoundError:
        return "Error: Image file not found. Check the file path."

def clean_text(text):
    """Cleans extracted text by removing unwanted characters."""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s,.-]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def extract_ingredients(text):
    """Extracts ingredients from OCR text."""
    match = re.search(r'ingredients:(.*?)(?:nutrition facts|frito-lay|$)', text, re.IGNORECASE)
    if match:
        ingredients = match.group(1).strip()
        return ingredients
    return "Ingredients not found"

def rank_food(ingredients):
    """Ranks food based on extracted ingredients."""
    bad_ingredients = ["high fructose corn syrup", "aspartame", "msg", "artificial flavors", "preservatives", "trans fat"]
    good_ingredients = ["whole grain", "fiber", "low sugar", "high protein"]

    ranking = "🟡 Moderate Choice"
    for ingredient in bad_ingredients:
        if ingredient.lower() in ingredients.lower():
            ranking = "🔴 Unhealthy (Avoid)"
            break

    for ingredient in good_ingredients:
        if ingredient.lower() in ingredients.lower():
            ranking = "🟢 Healthy (Best Choice)"
            break

    return ranking

def analyze_food(image_path):
    """Full pipeline: OCR -> Clean Text -> Extract Ingredients -> Rank Food"""
    extracted_text = extract_text(image_path)
    cleaned_text = clean_text(extracted_text)
    extracted_ingredients = extract_ingredients(cleaned_text)
    food_rank = rank_food(extracted_ingredients)

    # ✅ Display the final result in a clean format
    print("\n🔍 **Food Scan Results** 🔍")
    print("--------------------------------------------------")
    print(f"📜 **Extracted Text:**\n{extracted_text}")
    print("--------------------------------------------------")
    print(f"🍽️ **Ingredients Found:** {extracted_ingredients}")
    print("--------------------------------------------------")
    print(f"🏆 **Food Ranking:** {food_rank}")
    print("--------------------------------------------------")

# ✅ Run the complete food analysis system
image_path = r"C:\Users\sandhya\Documents\lays_packet.jpg"  # Update with correct image path
analyze_food(image_path)
