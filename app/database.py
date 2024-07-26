from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost/social-media-FastAPI"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

# Reference for connecting DB using psycopg2

# import psycopg2
# from  psycopg2.extras import RealDictCursor
# import time

# while True:
#   try:
#     connection = psycopg2.connect(host = "localhost", database = "social-media-FastAPI", user = "postgres", password = "postgres", cursor_factory = RealDictCursor)
#     cursor = connection.cursor()
#     print("Database connection successful...")
#     break
#   except Exception as error:
#     print("Database connection failed...")
#     print("Error: ", error)
#     time.sleep(3)