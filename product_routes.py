import os
from dotenv import load_dotenv
from supabase import create_client
from pydantic import BaseModel
from fastapi import FastAPI

load_dotenv()

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "SIH26090 backend is alive"}

class SignupRequest(BaseModel):
    email: str
    password: str

@app.post("/signup")
def signup(request: SignupRequest):
    response = supabase.auth.sign_up({
        "email": request.email,
        "password": request.password
    })

    return {
        "message": "Signup successful",
        "user": response.user
    }