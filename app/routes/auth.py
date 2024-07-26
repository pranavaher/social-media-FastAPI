from fastapi import status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2
from ..database import get_db

router = APIRouter(
  tags=["Auth"]
)

@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
  user = db.query(models.User).filter(models.User.email == user_credentials.username).filter().first()

  if not user:
    raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = f"Invalid credentials")

  if not utils.verify(user_credentials.password, user.password):
    raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = f"Invalid credentials")
  
  user_data = { "user_id": user.id }
  
  access_token = oauth2.create_access_token(user_data)
  return { "access_token": access_token, "token_type": "bearer" }

