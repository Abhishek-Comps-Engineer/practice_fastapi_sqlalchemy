
from .. import models, schema, utils
from typing import List
from sqlalchemy.orm import Session
from .. database import get_db
from fastapi import Body, FastAPI, Depends, HTTPException , status, APIRouter

router = APIRouter(
    prefix= "/users",
    tags=["Users"]
)

@router.post("/",status_code = status.HTTP_201_CREATED,response_model=schema.User)
def create_user(  user: schema.UserCreate, db: Session = Depends(get_db)):
 
    hashed_password = utils.hasing(user.password)
    print(hashed_password)
    user.password = hashed_password
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,   # 409 is standard for duplicate/conflict
            detail=f"User with email {user.email} already exists."
        )
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user




@router.get("/{id}",response_model=schema.User)
def get_user( id:int, db: Session = Depends(get_db)):
 
    existing_user = db.query(models.User).filter(models.User.id == id).first()
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,   # 409 is standard for duplicate/conflict
            detail=f"User with email {id} is not found."
        )
   
    return existing_user




@router.get("/",response_model=List[schema.User])
def get_user( db: Session = Depends(get_db)):
 
    existing_user = db.query(models.User).all()
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT   ,
            detail="User is not found."
        )
   
    return existing_user

    
