from models import UserInDB
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

fake_users_db ={
  "johndoe":{
    "username": "johndoe",
    "hashed_password": "hashedsecret"
  },
  "janedoe":{
    "username": "janedoe",
    "hashed_password": "hashedsecret2"
  }
}

def fakely_hashed_password(password: str):
  return f"hashed{password}"

def fake_token_generator(user:UserInDB)->str:
  return f"tokenized{user.username}"

def fake_token_resolver(token:str)->UserInDB | None:
  if token.startswith("tokenized"):
    user_id = token.removeprefix("tokenized")
    user = get_user(fake_users_db,user_id)
    return user

def get_user(db, username: str):
  if username in db:
    user_dict = db[username]
    return UserInDB(**user_dict)

def get_user_from_token(
    token: str= Depends(oauth2_scheme)
)->UserInDB:
  user = fake_token_resolver(token)
  if not user:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Invalid auth credentials",
      headers={"WWW-Authenticate": "Bearer"}
    )
  
  return user
