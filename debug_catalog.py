import os, json, io
from dotenv import load_dotenv
from google import genai
from supabase import create_client
from PIL import Image

load_dotenv()
genai_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

with open("tea set.jpg", "rb") as f:
    contents = f.read()

img = Image.open(io.BytesIO(contents))

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

response = genai_client.models.generate_content(
    model="gemini-3.6-flash",
    contents=[prompt, img],
    config={"response_mime_type": "application/json"}
)

print("RAW RESPONSE:", response.text)

cleaned = response.text.strip().strip("```json").strip("```").strip()
data = json.loads(cleaned)
print("PARSED:", data)

file_path = "tea set.jpg"
supabase.storage.from_("product-images").upload(file_path, contents)
data["image_url"] = supabase.storage.from_("product-images").get_public_url(file_path)
print("IMAGE URL:", data["image_url"])

result = supabase.table("products").insert(data).execute()
print("INSERT RESULT:", result)