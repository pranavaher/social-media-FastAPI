from fastapi import FastAPI, Response, status, HTTPException, Depends
from typing import Optional, List
from random import randrange
import psycopg2
from  psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

while True:
  try:
    connection = psycopg2.connect(host = "localhost", database = "social-media-FastAPI", user = "postgres", password = "postgres", cursor_factory = RealDictCursor)
    cursor = connection.cursor()
    print("Database connection successful...")
    break
  except Exception as error:
    print("Database connection failed...")
    print("Error: ", error)
    time.sleep(3)

my_posts = [
  {"id": 1, "title": "Game of Thrones", "Description": "Prince that was promised"},
  {"id": 2, "title": "House of Dragons", "Description": "Song of ice and fire"},
]

@app.get("/")
def root_route():
  return {"message": "dcdchhhhhhdcd" }

@app.get("/posts", response_model = List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
  # cursor.execute(""" SELECT * FROM posts """)
  # posts = cursor.fetchall()

  posts = db.query(models.Post).all()

  return posts

@app.post("/posts", status_code = status.HTTP_201_CREATED, response_model = schemas.PostResponse)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
  # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
  # new_post = cursor.fetchone()
  # connection.commit()

  new_post = models.Post(**post.model_dump())
  db.add(new_post)
  db.commit()
  db.refresh(new_post) # Get newly created post in new_post

  return new_post

@app.get("/posts/{id}", response_model = schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):
  # cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id)))
  # post = cursor.fetchone()

  post = db.query(models.Post).filter(models.Post.id == id).first()

  if not post:
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id {id} not found") 
  
  return post 
    
@app.put("/posts/{id}", status_code = status.HTTP_200_OK, response_model = schemas.PostResponse)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
  # cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, (post.title, post.content, post.published, str(id)))
  # updated_post = cursor.fetchone()
  # connection.commit()

  post = db.query(models.Post).filter(models.Post.id == id)

  if post.first() is None:
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id {id} not found")
  
  post.update(updated_post.model_dump(), synchronize_session=False)
  db.commit()

  return post.first()

@app.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
  # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (str(id)))
  # deleted_post = cursor.fetchone()
  # connection.commit()

  post = db.query(models.Post).filter(models.Post.id == id)

  if post.first() is None:
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id {id} not found")
  
  post.delete(synchronize_session=False)
  db.commit()

  return Response(status_code = status.HTTP_204_NO_CONTENT)

@app.post("/users", status_code = status.HTTP_201_CREATED, response_model = schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
  hashed_password = utils.hash(user.password)
  user.password = hashed_password
  
  new_user = models.User(**user.model_dump())
  db.add(new_user)
  db.commit()
  db.refresh(new_user) # Get newly created user in new_user

  return new_user