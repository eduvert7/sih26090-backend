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

from pydantic import BaseModel

class OrderRequest(BaseModel):
    product_id: int
    buyer_email: str
    quantity: int = 1
    amount: float

@router.post("/orders")
def create_order(request: OrderRequest):
    data = {
        "product_id": request.product_id,
        "buyer_email": request.buyer_email,
        "quantity": request.quantity,
        "amount": request.amount,
        "status": "pending"
    }
    result = supabase.table("orders").insert(data).execute()
    return {"message": "Order created", "data": result.data}


@router.get("/orders/{order_id}")
def get_order(order_id: int):
    response = supabase.table("orders").select("*").eq("id", order_id).execute()
    if not response.data:
        return {"error": "Order not found"}
    return response.data[0]


@router.get("/orders")
def get_all_orders():
    response = supabase.table("orders").select("*").execute()
    return response.data