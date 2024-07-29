from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import List, Optional
from sqlalchemy import func
from sqlalchemy.orm import Session
from ..database import engine, get_db
from .. import models, schemas, oauth2

router = APIRouter(
  prefix="/posts",
  tags=["Posts"]
)

@router.get("/", response_model=List[schemas.PostLikeResponse])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 100, skip: int = 0, search: Optional[str] = ""):

  # Restrict user to see own posts only
  
  # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

  # View All Posts

  posts = db.query(models.Post, func.count(models.Vote.post_id).label("likes")).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

  results = []
  for post, likes in posts:
    post_dict = {
      'id': post.id,
      'title': post.title,
      'content': post.content,
      'published': post.published,
      'created_at': post.created_at,
      'owner_id': post.owner_id,
      'owner': {
        'id': post.owner.id,
        'email': post.owner.email,
        'created_at': post.owner.created_at
      },
      'likes': likes
    }
    results.append(post_dict)

  return results

@router.post("/", status_code = status.HTTP_201_CREATED, response_model = schemas.PostResponse)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
  # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
  # new_post = cursor.fetchone()
  # connection.commit()

  new_post = models.Post(owner_id = current_user.id, **post.model_dump())
  db.add(new_post)
  db.commit()
  db.refresh(new_post) # Get newly created post in new_post

  return new_post

@router.get("/{id}", response_model = schemas.PostLikeResponse)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
  # cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id)))
  # post = cursor.fetchone()

  # post = db.query(models.Post).filter(models.Post.id == id).first()

  post, likes = db.query(models.Post, func.count(models.Vote.post_id).label("likes")).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first() 

  if not post:
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id {id} not found") 
  
  if post.owner_id != current_user.id:
    raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = f"You are not authorized to perform this action")
  
  post_dict = {
      'id': post.id,
      'title': post.title,
      'content': post.content,
      'published': post.published,
      'created_at': post.created_at,
      'owner_id': post.owner_id,
      'owner': {
        'id': post.owner.id,
        'email': post.owner.email,
        'created_at': post.owner.created_at
      },
      'likes': likes
    }
  
  post = post_dict
    
  return post 
    
@router.put("/{id}", status_code = status.HTTP_200_OK, response_model = schemas.PostResponse)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
  # cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, (post.title, post.content, post.published, str(id)))
  # updated_post = cursor.fetchone()
  # connection.commit()

  post_query = db.query(models.Post).filter(models.Post.id == id)
  post = post_query.first()
  
  if post is None:
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id {id} not found")
    
  if post.owner_id != current_user.id:
    raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = f"You are not authorized to perform this action")
  
  post_query.update(updated_post.model_dump(), synchronize_session=False)
  db.commit()

  return post

@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
  # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (str(id)))
  # deleted_post = cursor.fetchone()
  # connection.commit()

  post_query = db.query(models.Post).filter(models.Post.id == id)
  post = post_query.first()

  if post is None:
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id {id} not found")
  
  if post.owner_id != current_user.id:
    raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = f"You are not authorized to perform this action")

  
  post_query.delete(synchronize_session=False)
  db.commit()

  return Response(status_code = status.HTTP_204_NO_CONTENT)