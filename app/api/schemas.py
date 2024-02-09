from pydantic import BaseModel
from typing import List, Optional


class UserBase(BaseModel):
    username : str

class UserCreate(UserBase):
    password : str

class UserLogin(UserBase):
    password : str

class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    category: str
    sub_categories: List[str]
    image: str
class ProductCreate(ProductBase):
    pass

class ProductCatalogCreate(BaseModel):
    # Product fields
    name: str
    description: str
    price: float
    category: str
    sub_categories: List[str]
    variants: List[str]
    image: str

    # Catalog fields
    sku_id: str
    inv: int
    price: float
    discount_price: Optional[float] = None

    # User and Product IDs
    user_id: int
    pid: Optional[int] = 0

class CatalogItemBase(BaseModel):
    sku_id: str
    inv: int
    price: float
    discount_price: float
    variants: List[str]
    pid: int

class CatalogItemCreate(CatalogItemBase):
    pass
    
class CatalogItemResponse(CatalogItemBase):
    id: int

# class CatalogueResponse(BaseModel):
#     catalogue: List[CatalogueItem]

class InputData(BaseModel):
    input: str

class ProductDetail(BaseModel):
    name: str
    description: str
    price: float
    category: str
    sub_categories: List[str]
    image: str

class CatalogDetail(BaseModel):
    inv: int
    price: float
    discount_price: Optional[float] = None
    variants: List[str]

class ProductCatalogResponse(BaseModel):
    product: ProductDetail
    catalog: List[CatalogDetail] 