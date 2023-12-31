from fastapi import Response, status, HTTPException, Depends, APIRouter
from app import models, schemas, oauth2
from sqlalchemy.orm import Session
from app.database import engine, get_db
from typing import Optional, List

# this told the sql-achemy to create all the tables, we can remove it as we will be using alembic
# models.Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix="/vote", # add a prefix to our path based routing
    tags=["votes"]  # this adds a tag and this helps in documentation in swagger and fast-api http://lolcahost:8000/docs
)


@router.post("",status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db),
              current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {vote.post_id} does not exist")
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id,
                                              models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"user {current_user.id} already voted on post {vote.post_id}")
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="vote did not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "successfully delete vote"}
