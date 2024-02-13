from sqlalchemy import Column, Integer, String, Float, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)  # Correct
    products = relationship("Product", back_populates="owner")  

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    category = Column(String)
    sub_categories = Column(JSON)
    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="products") 
    catalogs = relationship("Catalog", back_populates="product")  

class Catalog(Base):
    __tablename__ = "catalogs"
    id = Column(Integer, primary_key=True)
    sku_id = Column(String)
    inv = Column(Integer)
    price = Column(Integer)
    discount_price = Column(Integer)
    variants = Column(JSON)
    image = Column(String)
    pid = Column(Integer, ForeignKey("products.id"))
    product = relationship("Product", back_populates="catalogs")



