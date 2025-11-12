import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from bson import ObjectId

from database import db, create_document, get_documents
from schemas import Product, Seller

app = FastAPI(title="VanVastra API", description="Handcrafted marketplace for artisans", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"name": "VanVastra", "message": "Welcome to VanVastra API"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    return response

# Helper for ObjectId string conversion
class ProductOut(BaseModel):
    id: str
    title: str
    description: Optional[str]
    price: float
    category: Optional[str]
    seller_name: Optional[str]
    image_base64: Optional[str]
    images: Optional[List[str]]
    in_stock: bool

# Create a product
@app.post("/products", response_model=dict)
def create_product_endpoint(product: Product):
    product_id = create_document("product", product)
    return {"id": product_id}

# List products
@app.get("/products", response_model=List[ProductOut])
def list_products(limit: int = 50):
    docs = get_documents("product", {}, limit)
    result: List[ProductOut] = []
    for d in docs:
        result.append(ProductOut(
            id=str(d.get("_id")),
            title=d.get("title"),
            description=d.get("description"),
            price=float(d.get("price", 0)),
            category=d.get("category"),
            seller_name=d.get("seller_name"),
            image_base64=d.get("image_base64"),
            images=d.get("images"),
            in_stock=bool(d.get("in_stock", True)),
        ))
    return result

# Simple seller create (optional for MVP)
@app.post("/sellers", response_model=dict)
def create_seller(seller: Seller):
    seller_id = create_document("seller", seller)
    return {"id": seller_id}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
