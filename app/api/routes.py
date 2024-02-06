from fastapi import APIRouter, Depends, HTTPException, Query,File, UploadFile
from sqlalchemy.orm import Session
# from app.api import schemas
# from app.api import auth, crud, deps, models
from app.api.utils import process_image, get_gemini_response
from fastapi.responses import JSONResponse
import logging
logger = logging.getLogger(__name__)

router = APIRouter()

# @router.post("/register")
# async def register(user: schemas.UserCreate, db: Session = Depends(deps.get_db)):
#     db_user = crud.get_user(db, username=user.username)
#     if db_user:
#         raise HTTPException(status_code=400, detail="Username already registered")
#     return crud.create_user(db=db, user=user)


# @router.post("/login")
# async def login(user: schemas.UserCreate, db: Session = Depends(deps.get_db)):
#     db_user = db.query(models.User).filter(models.User.username == user.username).first()
#     if not db_user or not auth.verify_password(user.password, db_user.password):
#         raise HTTPException(status_code=401, detail="Incorrect username or password")
#     return {"message": "Login successful"}

# @router.get("/catalogue/{user_id}", response_model=schemas.CatalogueResponse)
# def get_user_catalogue(user_id: int, db: Session = Depends(deps.get_db)):
#     catalogue_data = crud.get_catalogue_by_user_id(db, user_id=user_id)
#     if not catalogue_data:
#         raise HTTPException(status_code=404, detail="Catalogue data not found")
#     return {"catalogue": catalogue_data}

@router.post("/process_image/")
async def process_image_endpoint(
    uploaded_file: UploadFile = File(...)
):
    try:
        logger.info(f"Uploaded file name: {uploaded_file.filename}")
        logger.info(f"Uploaded file content type: {uploaded_file.content_type}")
        logger.info(f"Uploaded file size: {uploaded_file.file.__sizeof__()}")
        image_content = process_image(uploaded_file)
        logger.info(f"Processed image content: {image_content}")

        image_data = [{"mime_type": uploaded_file.content_type, "data": image_content}]
        #print(image_data)
        gemini_response = get_gemini_response(image_data)
        #print(gemini_response)
        return JSONResponse(content=gemini_response)#content={"response": gemini_response}
    except FileNotFoundError as e:
        logger.exception("FileNotFoundError occurred while processing the image")
        raise HTTPException(status_code=404, detail=str(e))
    
    
@router.post("/text_catalog/")
async def get_text_catalog(input: str):
    response = get_gemini_text(input)
    return JSONResponse(content=response)
