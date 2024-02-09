from sqlalchemy.orm import Session
from app.api import models,schemas,auth


def get_catalogue_by_user_id(db: Session, user_id: int):
    return db.query(models.Catalogue).filter(models.Catalogue.user_id == user_id).all()

def get_user(db, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(username=user.username, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Inside crud.py or similar module

def create_product(db: Session, item: schemas.CatalogItemCreate,user_id: int) -> models.Product:
    db_product = models.Product(
        name=item.name,
        description=item.description,
        category=item.category,
        sub_categories=item.sub_categories,
        image=item.image,
        user_id=user_id  # Assuming the user_id is part of the Product schema
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def create_catalog(db: Session, item: schemas.CatalogItemCreate, user_id: int) -> models.Catalog:
    db_catalog = models.Catalog(
        sku_id=item.sku_id,
        inv=item.inv,
        pid=item.pid,
        price=item.price,
        discount_price=item.discount_price,
        variants=item.variants,
        user_id=user_id
    )
    db.add(db_catalog)
    db.commit()
    db.refresh(db_catalog)
    return db_catalog

def get_products_by_user_id(db: Session, user_id: int):
    return db.query(models.Product).filter(models.Product.user_id == user_id).all()

def get_catalog_by_product_id(db: Session, product_id: int):
    return db.query(models.Catalog).filter(models.Catalog.pid == product_id).all()
