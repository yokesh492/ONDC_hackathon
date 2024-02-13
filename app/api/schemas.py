from pydantic import BaseModel
from typing import List, Optional, Dict, Any


class UserBase(BaseModel):
    username : str

class UserCreate(UserBase):
    password : str

class UserLogin(UserBase):
    password : str

class ProductBase(BaseModel):
    name: List[str]
    description: List[str]
    category: str
    sub_categories: List[str]
class ProductCreate(ProductBase):
    pass

class ProductCatalogCreate(BaseModel):
    # Product fields
    name: List[str]
    description: List[str]
    category: str
    sub_categories: List[str]
    

    # Catalog fields
    sku_id: str
    inv: int
    price: int
    discount_price: Optional[int] = None
    image: str
    variants: List[Dict[str, Any]]
    # User and Product IDs
    pid: Optional[int] = 0

class CatalogItemBase(BaseModel):
    sku_id: str
    inv: int
    price: int
    discount_price: int
    variants: List[Dict[str, Any]]
    pid: int
    image: str

class CatalogItemCreate(CatalogItemBase):
    pass
    
class CatalogItemResponse(CatalogItemBase):
    id: int

class InputData(BaseModel):
    input: str

class ProductDetail(BaseModel):
    id : int
    name: List[str]
    description: List[str]
    category: str
    sub_categories: List[str]
   
class CatalogDetail(BaseModel):
    catalogid : int
    inv: int
    price: int
    discount_price: Optional[int] = None
    variants: List[Dict[str, Any]]  
    image: str
class ProductCatalogResponse(BaseModel):
    product: ProductDetail
    catalog: List[CatalogDetail] 

class ProductCatalogDetail(BaseModel):
    product: ProductDetail
    catalog: CatalogDetail