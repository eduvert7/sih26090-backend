from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from product_route import router as product_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(product_router)

@app.get("/")
def read_root():
    return {"message": "SIH26090 backend is alive"}