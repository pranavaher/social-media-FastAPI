from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from  psycopg2.extras import RealDictCursor
import time

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
  return { "data": my_posts }

@app.post("/posts", status_code = status.HTTP_201_CREATED)
def create_post(post: Post):
  post_dict = post.model_dump()
  post_dict["id"] = len(my_posts) + 1
  my_posts.append(post_dict)

  return { "message": post_dict }

@app.get("/posts/{id}")
def get_post(id: int):
  post = find_post(id)

  if not post:
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id {id} not found") 
  
  return { "data": post }

def find_post(id):
  for post in my_posts:
    if post["id"] == id:
      return post

def find_post_index(id):
  for i, post in enumerate(my_posts):
    if post["id"] == id:
      return i
    
@app.put("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
def update_post(id: int, post: Post):
  index = find_post_index(id)

  if index is None:
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id {id} not found")
  
  post_dict = post.model_dump()
  post_dict["id"] = id
  my_posts[index] = post_dict

  return { "data": post_dict }

@app.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
  index = find_post_index(id)

  if index is None:
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id {id} not found")
  
  my_posts.pop(index)
  return Response(status_code = status.HTTP_204_NO_CONTENT)