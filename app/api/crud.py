from sqlalchemy.orm import Session
from app.api import models, schemas, auth
import json
from typing import Any

# User CRUD operations
def get_user(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(username=user.username, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Product CRUD operations
def create_product(db: Session, item: schemas.ProductCatalogCreate, user_id: int) -> models.Product:
    db_product = models.Product(
        name=item.name,
        description=item.description,
        category=item.category,
        sub_categories=item.sub_categories,
        user_id=user_id
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_products_by_user_id(db: Session, user_id: int):
    return db.query(models.Product).filter(models.Product.user_id == user_id).all()

def get_product_by_id(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

# Catalog CRUD operations
def create_catalog(db: Session, item: schemas.ProductCatalogCreate, user_id: int) -> models.Catalog:
    db_catalog = models.Catalog(
        sku_id=item.sku_id,
        inv=item.inv,
        pid=item.pid,
        price=item.price,
        discount_price=item.discount_price,
        variants=item.variants,
        image=item.image,
    )
    db.add(db_catalog)
    db.commit()
    db.refresh(db_catalog)
    return db_catalog

def get_catalog_by_id(db: Session, catalog_id: int):
    return db.query(models.Catalog).filter(models.Catalog.id == catalog_id).first()

def get_catalog_by_product_id(db: Session, product_id: int):
    return db.query(models.Catalog).filter(models.Catalog.pid == product_id).all()

def delete_product_and_catalogs(db: Session, catalog_id: int) -> Any:
    catalog = db.query(models.Catalog).filter(models.Catalog.id == catalog_id).first()
    if catalog is None:
        return {"message": "Catalog not found"}
    
    product_id = catalog.pid
    db.delete(catalog)
    db.commit()
    
    other_catalogs = db.query(models.Catalog).filter(models.Catalog.pid == product_id).all()
    if not other_catalogs:
        db.query(models.Product).filter(models.Product.id == product_id).delete()
        db.commit()
    
    return {"message": "Catalog and, if applicable, product deleted successfully"}
