from fastapi.encoders import jsonable_encoder
from db.session import SessionLocal
from typing import AsyncGenerator
from typing import  Optional,Generator
from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from pydantic import BaseModel
from sqlalchemy.orm.session import Session
from core.auth import oauth2_scheme
from core.config import settings
from db.session import SessionLocal
import crud
from models.user import User
from core.auth_bearer import jwt_bearer,decodeJWT
from models.token import TokenData

# class TokenData(BaseModel):
#     username: Optional[str] = None

# async def get_db() -> AsyncGenerator:
#     async with SessionLocal() as session:
#         yield session
def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(
    db: Session = Depends(get_db), 
    token: str = Depends(jwt_bearer)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decodeJWT(token)
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(id=user_id)
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.email == token_data.id).first()
    if user is None:
        raise credentials_exception
    token_data = db.query(TokenData).filter(TokenData.token == token).first()
    if token_data is None or not token_data.is_active:
        raise credentials_exception
    return user

def get_current_active_manager(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != "manager":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return current_user
def get_current_active_superuser(
    current_user: User = Depends(get_current_user),
) -> User:
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user