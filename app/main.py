from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from  psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

class Post(BaseModel):
  title: str
  content: str
  published: bool = True

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

@app.get("/posts")
def get_posts():
  cursor.execute(""" SELECT * FROM posts """)
  posts = cursor.fetchall()

  return { "data": posts }

@app.post("/posts", status_code = status.HTTP_201_CREATED)
def create_post(post: Post):
  cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))

  new_post = cursor.fetchone()
  
  connection.commit()
  return { "message": new_post }

@app.get("/posts/{id}")
def get_post(id: int):
  cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id)))
  post = cursor.fetchone()

  if not post:
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id {id} not found") 
  
  return { "data": post }
    
@app.put("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
def update_post(id: int, post: Post):
  cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, (post.title, post.content, post.published, str(id)))

  updated_post = cursor.fetchone()

  if updated_post is None:
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id {id} not found")

  connection.commit()
  return { "data": updated_post }

@app.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
  cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (str(id)))
  deleted_post = cursor.fetchone()


  if deleted_post is None:
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id {id} not found")

  connection.commit()
  return Response(status_code = status.HTTP_204_NO_CONTENT)