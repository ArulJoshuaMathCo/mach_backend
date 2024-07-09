from typing import Any

from fastapi import APIRouter, Depends, HTTPException,status
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
from models.user import User
from models.token import TokenData
from sqlalchemy.future import select
from core.auth_bearer import jwt_bearer
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
    
    access_token = create_access_token(sub=user.id)
    refresh_token = create_refresh_token(sub=user.id)

    token_in = TokenData(id=user.id, token=access_token, refresh_token=refresh_token, is_active=True)
    crud.crud_token.token.create(db=db, token_in=token_in)

    return {
        "access_token": create_access_token(sub=user.id),
        "refresh_token": create_refresh_token(sub=user.id),
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
                #   current_user: User = Depends(deps.get_current_user)
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
    # current_user: User = Depends(deps.get_current_active_manager)
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
    user = crud.user.create(db=db, obj_in=user_in)

    return user

'''
Using scopes for authorization
Refresh tokens
Password resets
Single Sign On (SSO)
Adding custom data to the JWT payload
JSON Web Encryption
'''