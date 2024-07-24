from fastapi import FastAPI
import psycopg2
from  psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine
from .routes import post, user

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(post.router)
app.include_router(user.router)

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

@app.get("/")
def root_route():
  return {"message": "dcdchhhhhhdcd" }
