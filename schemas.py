"""
Database Schemas for VanVastra

Each Pydantic model represents a collection in MongoDB. The collection name
is the lowercase of the class name.

- Seller -> "seller"
- Product -> "product"
"""

from pydantic import BaseModel, Field
from typing import Optional, List

class Seller(BaseModel):
    name: str = Field(..., description="Seller display name")
    email: Optional[str] = Field(None, description="Contact email")
    phone: Optional[str] = Field(None, description="Contact phone number")
    city: Optional[str] = Field(None, description="City or region")
    bio: Optional[str] = Field(None, description="Short bio about the artisan")
    avatar_url: Optional[str] = Field(None, description="Profile image URL or base64 data URL")

class Product(BaseModel):
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in currency units")
    category: Optional[str] = Field(None, description="Category like textiles, pottery, jewelry, etc.")
    seller_name: Optional[str] = Field(None, description="Name of the seller/brand")
    image_base64: Optional[str] = Field(None, description="Primary image as base64 data URL for simplicity")
    images: Optional[List[str]] = Field(default=None, description="Optional gallery of images as base64 data URLs")
    in_stock: bool = Field(True, description="Whether product is in stock")
