from fastapi import Response, status, HTTPException, Depends, APIRouter
from app import models, schemas, oauth2
from sqlalchemy.orm import Session
from app.database import engine, get_db
from typing import Optional, List
from sqlalchemy import func

# this told the sql-achemy to create all the tables, we can remove it as we will be using alembic
# models.Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix="/posts", # add a prefix to our path based routing
    tags=["posts"]  # this adds a tag and this helps in documentation in swagger and fast-api http://lolcahost:8000/docs
)


@router.get("/")
def root():
    return {"message": "Hello World!"}

#@router.get("", response_model=list[schemas.PostOut])


@router.get("", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db),
              current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0,
              search: Optional[str] = ""):
    # db.query(models.Post) --> this will just return the SQL query. And if add .all() then it will be
    # executed against postgres to fetch all.
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # Get posts along with the votes each post got, we will be performing joins on posts and votes table.
    posts = (db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote,
                 models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id)
               .filter(models.Post.title.contains(search)).limit(limit).offset(skip).all())
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    return posts


@router.post("", status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):
    # # this is a staging change to the postgres sql databases
    # cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s, %s, %s) RETURNING * """,
    #                (post.title,post.content,post.published))
    # new_post = cursor.fetchone()
    # # commit to actually store the value in postgres sql database
    # conn.commit()

    # new_post = models.Post(title=post.title,content=post.content,published=post.published)
    # we will convert our post pydantic model to dictionary, and the unpack it like **post.dict()

    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post) # add the post data to DB
    db.commit() # Save the data in DB
    db.refresh(new_post) # retrieve the saved data and store it in new_post variable, similar to 'RETURNING *'
    return new_post


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db),
             current_user: int = Depends(oauth2.get_current_user)): # this : int makes sure that id is converted to integer
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    # post = cursor.fetchone()
    #post = db.query(models.Post).filter(models.Post.id == id).first()
    post = (db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote,
                 models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id)
            .filter(models.Post.id == id).first())
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                             detail="Not Authorized to perform this action")
    post_query.delete(synchronize_session=False)
    db.commit()
    print(f"Deleted post: {post_query.first()}")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #                (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if not post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    print(f"Updated post: {post_query.first()}")
    return post_query.first()
