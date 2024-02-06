from pydantic import BaseModel
from typing import List


class UserBase(BaseModel):
    username : str

class UserCreate(UserBase):
    password : str

class UserLogin(UserBase):
    password : str

class CatalogueItem(BaseModel):
    name: str
    description: str
    price: float
    qty: int
    image: str

class CatalogueResponse(BaseModel):
    catalogue: List[CatalogueItem]

class InputData(BaseModel):
    input: str
