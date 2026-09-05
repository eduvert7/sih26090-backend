from fastapi import APIRouter
from supabase import create_client
import os
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

router = APIRouter()

class SignupRequest(BaseModel):
    email: str
    password: str

@router.post("/signup")
def signup(request: SignupRequest):
    response = supabase.auth.sign_up({
        "email": request.email,
        "password": request.password
    })
    return {"message": "Signup successful", "user": response.user}
