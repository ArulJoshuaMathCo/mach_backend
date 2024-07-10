import datetime
import re
from typing import Any
from jwt import encode,decode
import logging
from schemas.user import UserInDB
from fastapi import APIRouter, Depends, HTTPException,status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session
import crud
import crud.crud_token
import schemas
from api import deps
from core.auth import (
    authenticate,
    create_access_token,create_refresh_token
)
from schemas.token import TokenRequest
from models.user import User
from models.token import TokenData
from core.security import get_password_hash
from sqlalchemy.future import select
from core.auth_bearer import jwt_bearer,decodeJWT
router = APIRouter()


@router.post("/login")
def login(
    db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    Get the JWT for a user with data from OAuth2 request form body.
    """

    user = authenticate(email=form_data.username, password=form_data.password, db=db)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(sub=user.email)
    refresh_token = create_refresh_token(sub=user.email)

    token_in = TokenData(id=user.id, token=access_token, refresh_token=refresh_token, is_active=True)
    crud.crud_token.token.create(db=db, token_in=token_in)

    return {
        "access_token": create_access_token(sub=user.email),
        "refresh_token": create_refresh_token(sub=user.email),
        "token_type": "bearer",
    }

@router.post("/logout")
async def logout(token: str = Depends(jwt_bearer), db: Session = Depends(deps.get_db)):
    # Fetch the token data
    result = db.execute(select(TokenData).where(TokenData.token == token))
    token_data = result.scalars().first()
    
    if token_data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Token not found")

    # Set is_active to False
    token_data.is_active = False
    db.add(token_data)
    db.commit()

    return {"msg": "Successfully logged out"}
@router.get("/me", response_model=schemas.User)
def read_users_me(current_user: User = Depends(deps.get_current_user)):
    """
    Fetch the current logged in user.
    """

    user = current_user
    return user

from typing import List
@router.get("/all", response_model=List[schemas.User])
async def read_users_all(db:Session= Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_manager)
                  ):
    """
    Fetch the current logged in user.
    """

    users= await crud.user.get_multi(db=db)
    return users


@router.put("/{user_id}/role", response_model=schemas.User)
async def update_role(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
    role: str,
    current_user: User = Depends(deps.get_current_active_manager)
) -> Any:
    """
    Update a user's role.
    """
    user = await crud.user.get(db=db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user_in = schemas.user.UserUpdate(role=role)
    user = crud.user.update(db=db, db_obj=user, obj_in=user_in)
    return user

@router.post("/signup", response_model=schemas.User, status_code=201)
def create_user_signup(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.user.UserCreate,
) -> Any:
    """
    Create new user without the need to be logged in.
    """

    user = db.query(User).filter(User.email == user_in.email).first()
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system",
        )
    regex = r"\b[A-Za-z0-9._%+-]+@mathco+\.[A-Z|a-z]{2,}\b"
    email= user_in.email
    if not re.fullmatch(regex, email):
        raise HTTPException(status_code=400,detail="error: mail does not belong to the organization")
    user = crud.user.create(db=db, obj_in=user_in)

    return user
secret = "55f6801c3187b2360340a676788b6bff"
@router.post("/callback")
async def microsoft_callback(token_request: TokenRequest, db: Session = Depends(deps.get_db)):
    token = token_request.token

    try:
        user_data = decode_token(token)
        email = user_data.get("preferred_username")
        first_name = user_data.get("name")
        surname = " "
        is_superuser = False
        roles= "user"
        # Generate a dummy password if not provided
        hashed_password = get_password_hash("12345678")
        # Check if user already  exists
        user = db.query(User).filter(User.email == email).first()
        if not user:
            user = User(
                email=email,
                first_name=first_name,
                surname=surname,
                is_superuser=is_superuser,
                hashed_password=hashed_password,
                role=roles,
            )
            db.add(user)
            db.commit()
        else:
            user.first_name = first_name
            user.surname = surname
            user.is_superuser = is_superuser
            db.commit()

        access_token = create_access_token(sub=user.email)
        refresh_token = create_refresh_token(sub=user.email)
        token_in = TokenData(id=user.id, token=access_token, refresh_token=refresh_token, is_active=True)
        crud.crud_token.token.create(db=db, token_in=token_in)
        return JSONResponse(content={"access_token": access_token}, status_code=status.HTTP_200_OK)

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))



def encode_payload(
    payload: dict, secret: str = secret, algorithm: str = "RS256"
) -> str:
    return encode(payload, secret, algorithm=algorithm)
def decode_token(token: str):
    try:
        return decode(
            jwt=token,
            key=None,
            algorithms=['RS256'],
            options={"verify_signature": False},
        )
    except Exception as e:
        logging.exception(e)
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            message={"error"},
        )

'''
Using scopes for authorization
Refresh tokens
Password resets
Single Sign On (SSO)
Adding custom data to the JWT payload
JSON Web Encryption
'''