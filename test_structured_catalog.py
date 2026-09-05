import os
from dotenv import load_dotenv
from google import genai
from PIL import Image
import json

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

img = Image.open("tea set.jpg")

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

response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=[prompt, img],
    config={"response_mime_type": "application/json"}
)

print(response.text)
data = json.loads(response.text)
print(data["title"])
print(data["tags"])