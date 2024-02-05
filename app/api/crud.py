# from sqlalchemy.orm import Session
# from app.api import models,schemas,auth


# def get_catalogue_by_user_id(db: Session, user_id: int):
#     return db.query(models.Catalogue).filter(models.Catalogue.user_id == user_id).all()

# def get_user(db, username: str):
#     return db.query(models.User).filter(models.User.username == username).first()

# def create_user(db: Session, user: schemas.UserCreate):
#     hashed_password = auth.get_password_hash(user.password)
#     db_user = models.User(username=user.username, password=hashed_password)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user
