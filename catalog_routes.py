from fastapi import APIRouter, UploadFile, File
from google import genai
from supabase import create_client
import os, json, io, time, uuid
from dotenv import load_dotenv
from PIL import Image

load_dotenv()
genai_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

router = APIRouter()

# Set to True to bypass Gemini and test the storage/database pipeline independently
USE_FAKE_DATA = False

@router.post("/catalog", summary="Catalog a product from an image", description="Upload a product image to generate an AI-written title, description, tags, and artisan story, then save it to the database.")
async def catalog_product(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        img = Image.open(io.BytesIO(contents))
        img.thumbnail((800, 800))

        if USE_FAKE_DATA:
            data = {
                "title": "Handwoven Ceramic Tea Set",
                "description": "A beautiful handcrafted tea set made using traditional pottery techniques.",
                "tags": "ceramic, handmade, tea set, pottery, artisan",
                "story": "This tea set carries generations of craft tradition, shaped by hand on a potter's wheel."
            }
        else:
            prompt = """
            Analyze this product image, made by a marginalized artisan for an online marketplace.
            Return ONLY valid JSON with this exact structure, no extra text:
            {
              "title": "short catchy product title",
              "description": "2-3 sentence marketplace description",
              "tags": "comma-separated list of 4-5 relevant tags",
              "story": "a short 3-4 sentence story about the craft/artisan tradition behind this type of product"
            }
            """

            response = None
            for attempt in range(3):
                try:
                    response = genai_client.models.generate_content(
                        model="gemini-flash-latest",
                        contents=[prompt, img],
                        config={"response_mime_type": "application/json"}
                    )
                    break
                except Exception as e:
                    time.sleep(10)

            if response is None:
                return {"error": "AI service is temporarily busy. Please try again in a moment."}

            cleaned = response.text.strip().strip("```json").strip("```").strip()
            data = json.loads(cleaned)

        file_path = f"{uuid.uuid4()}_{file.filename}"
        supabase.storage.from_("product-images").upload(file_path, contents)
        data["image_url"] = supabase.storage.from_("product-images").get_public_url(file_path)

        supabase.table("products").insert(data).execute()
        return {"message": "Product cataloged", "data": data}

    except json.JSONDecodeError:
        return {"error": "AI response could not be parsed. Please try again."}
    except Exception as e:
        return {"error": str(e)}