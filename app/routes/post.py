from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import List
from sqlalchemy.orm import Session
from ..database import engine, get_db
from .. import models, schemas, oauth2

router = APIRouter(
  prefix="/posts",
  tags=["Posts"]
)

@router.get("/", response_model = List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
  # cursor.execute(""" SELECT * FROM posts """)
  # posts = cursor.fetchall()

  posts = db.query(models.Post).all()

  return posts

@router.post("/", status_code = status.HTTP_201_CREATED, response_model = schemas.PostResponse)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
  # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
  # new_post = cursor.fetchone()
  # connection.commit()

  new_post = models.Post(**post.model_dump())
  db.add(new_post)
  db.commit()
  db.refresh(new_post) # Get newly created post in new_post

  return new_post

@router.get("/{id}", response_model = schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
  # cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id)))
  # post = cursor.fetchone()

  post = db.query(models.Post).filter(models.Post.id == id).first()

  if not post:
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id {id} not found") 
  
  return post 
    
@router.put("/{id}", status_code = status.HTTP_200_OK, response_model = schemas.PostResponse)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
  # cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, (post.title, post.content, post.published, str(id)))
  # updated_post = cursor.fetchone()
  # connection.commit()

  post = db.query(models.Post).filter(models.Post.id == id)

  if post.first() is None:
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id {id} not found")
  
  post.update(updated_post.model_dump(), synchronize_session=False)
  db.commit()

  return post.first()

@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
  # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (str(id)))
  # deleted_post = cursor.fetchone()
  # connection.commit()

  post = db.query(models.Post).filter(models.Post.id == id)

  if post.first() is None:
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id {id} not found")
  
  post.delete(synchronize_session=False)
  db.commit()

  return Response(status_code = status.HTTP_204_NO_CONTENT)