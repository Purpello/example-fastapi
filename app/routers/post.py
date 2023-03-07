from .. import models, schemas, oauth2
from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional

router = APIRouter(
    prefix = "/posts",
    tags = ['Posts'] # affects the docs
)

@router.get("/",response_model = List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db),
              limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    #skip+offset is how we'll implement pagination
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    #Get the votes data.  Going to do some left joins
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")
        ).join(
            models.Vote, models.Vote.post_id == models.Post.id, isouter=True
        ).group_by(
            models.Post.id
        ).all()

    return results

@router.post("/", status_code=status.HTTP_201_CREATED,response_model = schemas.Post)
def create_posts(post: schemas.PostCreate, response: Response,db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):

    #print(current_user.email) #don't really need this, just showing how we have the user object from the oauth stuff.
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}",response_model = schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"There is no post number {id}")
    
    return post

@router.delete("/{id}",status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int, response: Response,db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):

    query_post = db.query(models.Post).filter(models.Post.id == id)

    post = query_post.first()

    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id {id} was not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can only delete your own posts")

    query_post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",status_code=status.HTTP_200_OK,response_model = schemas.Post)
def update_post(id: int, post: schemas.PostCreate, response: Response,db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    
    query_post = db.query(models.Post).filter(models.Post.id == id)
    updated_post = query_post.first()

    if updated_post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                            detail = f"Post with id {id} was not found")
    
    if updated_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can only update your own posts")
    
    query_post.update(post.dict(), synchronize_session=False)
    db.commit()

    return query_post.first()