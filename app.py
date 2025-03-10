from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import pytesseract
import re
from PIL import Image, ImageEnhance, ImageFilter
import io

# ✅ Set the correct Tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# ✅ Create FastAPI App
app = FastAPI()

# ✅ Enable CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from all origins (Change this to your frontend URL for better security)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# ✅ Define the `/upload/` endpoint
@app.post("/upload/")
async def analyze_food(file: UploadFile = File(...)):
    """Allows users to upload an image and get food ranking results."""
    image = Image.open(io.BytesIO(await file.read()))
    
    # Preprocess the image
    image = image.convert("L")
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2.0)
    image = image.filter(ImageFilter.EDGE_ENHANCE)

    # Perform OCR
    extracted_text = pytesseract.image_to_string(image)

    # Clean text
    def clean_text(text):
        text = text.lower()
        text = re.sub(r'[^a-z0-9\s,.-]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    cleaned_text = clean_text(extracted_text)

    # Extract ingredients
    def extract_ingredients(text):
        match = re.search(r'ingredients:(.*?)(?:nutrition facts|frito-lay|$)', text, re.IGNORECASE)
        return match.group(1).strip() if match else "Ingredients not found"

    extracted_ingredients = extract_ingredients(cleaned_text)

    # Rank food
    def rank_food(ingredients):
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
    
    food_rank = rank_food(extracted_ingredients)

    return {
        "Extracted Text": extracted_text,
        "Ingredients": extracted_ingredients,
        "Food Ranking": food_rank
    }

# ✅ Add a simple homepage
@app.get("/")
def home():
    return {"message": "CORS Fixed! Welcome to the AI Food Scanner API! Go to /docs to upload an image."}
