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


class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/login")
def login(request: LoginRequest):
    response = supabase.auth.sign_in_with_password({
        "email": request.email,
        "password": request.password
    })
    return {
        "message": "Login successful",
        "access_token": response.session.access_token
    }


@router.get("/products")
def get_products():
    response = supabase.table("products").select("*").execute()
    return response.data


@router.get("/products/{product_id}")
def get_product(product_id: int):
    response = supabase.table("products").select("*").eq("id", product_id).execute()
    if not response.data:
        return {"error": "Product not found"}
    return response.data[0]