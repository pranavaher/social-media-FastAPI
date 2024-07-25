from jose import jwt, JWTError
from datetime import datetime, timedelta

SECRET_KEY = "6e9ff96bec95c5177f1365125edae0ee7ee9769cd7b27edb5082ffe0487b9114"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
  to_encode = data.copy()

  expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  to_encode.update({ "exp": expire })

  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

  return encoded_jwt
