import os
from dotenv import load_dotenv
from google import genai
from PIL import Image

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

img = Image.open("images.jpg")

response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=[
        "Describe this product in one sentence, as if for an online marketplace listing.",
        img
    ]
)

print(response.text)