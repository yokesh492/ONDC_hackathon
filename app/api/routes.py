from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from app.api import schemas, auth, crud, deps, models
from app.api.utils import (
    process_image,
    get_gemini_response,
    get_gemini_text,
    upload_image_vps_bucket,
    convert_variants_format
)
from fastapi.responses import JSONResponse
import json
import logging
from typing import List

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/register")
async def register(user: schemas.UserCreate, db: Session = Depends(deps.get_db)):
    db_user = crud.get_user(db, username=user.username)
    if db_user:
        return {"message": "Username already registered"}
    return crud.create_user(db=db, user=user)

@router.post("/login")
async def login(user: schemas.UserCreate, db: Session = Depends(deps.get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if not db_user or not auth.verify_password(user.password, db_user.password):
        return {"message": "Incorrect username or password"}
    return {"user_id": db_user.id, "message": "Login successful"}

@router.post("/process_image/")
async def process_image_endpoint(uploaded_file: UploadFile = File(...)):
    try:
        image_url = await upload_image_vps_bucket(uploaded_file)
        image_content = process_image(uploaded_file)
        logger.info(f"Processed image content: {image_content}")
        image_data = [{"mime_type": uploaded_file.content_type, "data": image_content}]
        gemini_response = await get_gemini_response(image_data)
        gemini_response['image'] = image_url
        return JSONResponse(content=gemini_response)
    except FileNotFoundError as e:
        logger.exception("FileNotFoundError occurred while processing the image")
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/text_catalog/")
async def get_text_catalog(input_data: schemas.InputData):
    response = await get_gemini_text(input_data.input)
    return JSONResponse(content=response)

@router.post("/add_to_catalog/{user_id}")
def create_catalogue_item(user_id: int, item: schemas.ProductCatalogCreate, db: Session = Depends(deps.get_db)):
    if item.pid == 0:
        product = crud.create_product(db=db, item=item, user_id=user_id)
        item.pid = product.id
    catalog_entry = crud.create_catalog(db=db, item=item, user_id=user_id)
    return catalog_entry

@router.get("/catalogue/{user_id}", response_model=List[schemas.ProductCatalogResponse])
def get_user_catalogue(user_id: int, db: Session = Depends(deps.get_db)):
    products = crud.get_products_by_user_id(db, user_id=user_id)
    if not products:
        return JSONResponse(status_code=200, content={"message": "No products found for the user. Please add a catalog."})

    catalogue_data = []
    for product in products:
        catalog_items = crud.get_catalog_by_product_id(db, product_id=product.id)
        product_details = schemas.ProductDetail(**product.__dict__)

        catalog_details_list = []
        for catalog_item in catalog_items:
            variants = catalog_item.variants
            if isinstance(variants, str):
                variants = json.loads(variants)
            variants = convert_variants_format(variants)
            catalog_details_data = {
                "catalogid": catalog_item.id,
                "inv": catalog_item.inv,
                "price": catalog_item.price,
                "discount_price": catalog_item.discount_price,
                "variants": variants,
                "image": catalog_item.image,
            }
            catalog_details = schemas.CatalogDetail(**catalog_details_data)
            catalog_details_list.append(catalog_details)

        product_catalog_response = schemas.ProductCatalogResponse(
            product=product_details,
            catalog=catalog_details_list
        )
        catalogue_data.append(product_catalog_response)

    return catalogue_data

@router.get("/catalog_detail/{catalog_id}", response_model=schemas.ProductCatalogDetail)
def get_product_catalog_detail(catalog_id: int, db: Session = Depends(deps.get_db)):
    catalog = crud.get_catalog_by_id(db, catalog_id=catalog_id)
    if not catalog:
        raise HTTPException(status_code=404, detail="Catalog not found")
    product = crud.get_product_by_id(db, product_id=catalog.pid)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found associated with the catalog")
    variants = catalog.variants
    if isinstance(variants, str):
        variants = json.loads(variants)
    variants = convert_variants_format(variants)
    catalog_details_data = {
        "catalogid": catalog.id,
        "inv": catalog.inv,
        "price": catalog.price,
        "discount_price": catalog.discount_price,
        "variants": variants,
        "image": catalog.image
    }
    return {"catalog": catalog_details_data, "product": product}

@router.post("/create_catalog/{user_id}")
def create_catalogue_item(user_id: int, item: schemas.ProductCatalogCreate, db: Session = Depends(deps.get_db)):
    catalog_entry = crud.create_catalog(db=db, item=item, user_id=user_id)
    return catalog_entry

@router.delete("/product/{catalog_id}")
def delete_product(catalog_id: int, db: Session = Depends(deps.get_db)):
    crud.delete_product_and_catalogs(db, catalog_id=catalog_id)
    return {"detail": "Product and related catalog entries deleted successfully"}


# @router.get("/products/{product_id}", response_model=schemas.ProductDetail)
# def get_product_detail(product_id: int, db: Session = Depends(deps.get_db)):
#     product = db.query(models.Product).filter(models.Product.id == product_id).first()
#     if product is None:
#         raise HTTPException(status_code=404, detail="Product not found")
#     return product

