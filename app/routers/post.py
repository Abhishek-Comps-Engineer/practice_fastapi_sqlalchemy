from .. import models, schema, utils
from typing import List, Optional
from sqlalchemy.orm import Session
from .. database import get_db
from fastapi import Body, FastAPI, Depends, HTTPException , status, APIRouter
from . import oauth2
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


# get all post
# @router.get("/",response_model=List[schema.Post])
@router.get("/",response_model=List[schema.PostOut])
def get_posts(db: Session = Depends(get_db),current_user:  int  = Depends(oauth2.get_current_user),
              limit: int = 10, skip: int = 0, search: Optional[str] = ""):
   
#    data = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

   results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(
             models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
   
   return results


@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schema.Post)
def create_post(post: schema.PostCreate ,db: Session = Depends(get_db),
                 current_user:  int  = Depends(oauth2.get_current_user)):
    
    db_post = models.Post(owner_id = current_user.id, **post.__dict__)
    # print(post.__dict__)
    print(current_user.email) 
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


# single post retrieving
@router.get("/{post_id}", response_model=schema.PostOut)
def get_post(post_id: int, db: Session = Depends(get_db), 
             current_user:  int  = Depends(oauth2.get_current_user)):
    
    # db_post = db.query(models.Post).filter(models.Post.id == post_id).first()

    db_post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(
             models.Post.id).filter(models.Post.id == post_id).first()

    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    post, votes = db_post
    
    if post.owner_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail = f"Not Authorized to perform the reuested action")
    return db_post


@router.delete("/{post_id}", response_model=None)
def delete_post(post_id: int, db: Session = Depends(get_db), 
                current_user:  int  = Depends(oauth2.get_current_user)):
    db_post = db.query(models.Post).filter(models.Post.id == post_id)
    new_post = db_post.first()

    if not new_post:
        raise HTTPException(status_code=404, detail="Post not found")

    if new_post.owner_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail = f"Not Authorized to perform the reuested action")
    
    db_post.delete(synchronize_session=False)
    db.commit()
    # return f"Post Deleted Successfully ${db_post.__dict__}"   correct
    return { "Post Deleted Successfully "}   



@router.put("/{post_id}", response_model=schema.Post)
def update_post(post_id: int, post : schema.PostCreate,db: Session = Depends(get_db), 
                current_user:  int  = Depends(oauth2.get_current_user)):
    db_post = db.query(models.Post).filter(models.Post.id == post_id)
    new_post = db_post.first()

    if not new_post:
        raise HTTPException(status_code=404, detail="Post not found")
     
    # print("current_user:", current_user.id)
    # print("post owner_id:", new_post.owner_id)

    if new_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail = f"Not Authorized to perform the reuested action")
    db_post.update(post.dict(), synchronize_session=False)
    db.commit()
    db.refresh(new_post)
    # return f"Post Deleted Successfully ${db_post.__dict__}"   correct
    return new_post  

