from app.routers import oauth2
from .. import models, schema, utils
from typing import List
from sqlalchemy.orm import Session
from .. database import get_db
from fastapi import Body, FastAPI, Depends, HTTPException , status, APIRouter

router = APIRouter(
    prefix= "/votes",
    tags=["Votes"]
)


@router.post("/",status_code=status.HTTP_201_CREATED)
def vote(vote: schema.Vote, db:Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
   
   post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
   
   if not post:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                          detail=f"Post id {vote.post_id} is not exist")
   
   vote_query = db.query(models.Vote).filter(models.Vote.user_id == current_user.id, models.Vote.post_id == vote.post_id)
   found_vote = vote_query.first()

 
   if ( vote.dir == 1):
      if found_vote :
         raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                             detail=f"User {current_user.id} is already voted the post." )
      
      new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
      db.add(new_vote)
      db.commit()
      return {"message":"Successfully Voted"}
   else:
      if not found_vote:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"Vote doesn't exist")
      vote_query.delete(synchronize_session=False)
      db.commit()
      return {"message":"Vote deleted Successffully"}


@router.get("/")
def get_votes(db : Session = Depends(get_db)):
   pass