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


from fastapi_sso.sso.microsoft import MicrosoftSSO
from starlette.requests import Request
from dotenv import load_dotenv
from fastapi.responses import RedirectResponse
from core.auth import create_access_token
import os
from urllib.parse import urlencode
import requests
SESSION_COOKIE_NAME='access_token'
OAUTH_TENANT = '4bf30310-e4f1-4658-9e34-9e8a5a193ed1'
OAUTH_APPLICATION_ID = 'aa4b401e-421b-426d-a170-f8f50e7c8028'
OAUTH_CLIENT_SECRET = 'a3c0958bb2bc8dd0be54b6c99f86a10449bbdc494aab440a5d7f93b642dea007'
REDIRECT_URI = f"http://127.0.0.1:8000/auth/callback"

AUTHORITY = f"https://login.microsoftonline.com/{OAUTH_TENANT}"
AUTHORIZE_URL = f"{AUTHORITY}/oauth2/v2.0/authorize"
TOKEN_URL = f"{AUTHORITY}/oauth2/v2.0/token"
USER_INFO_URL = "https://graph.microsoft.com/v1.0/me"

# router = APIRouter(prefix="/v1/microsoft")

@router.get("/mlogin")
async def microsoft_login():
    params = {
        "client_id": OAUTH_APPLICATION_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "response_mode": "query",
        "scope": "openid User.Read email",
        "state": "12345"  # You can use a more secure method to generate state
    }
    url = f"{AUTHORIZE_URL}?{urlencode(params)}"
    print(url)
    return RedirectResponse(url)

@router.get("/callback")
async def microsoft_callback(request: Request, db: Session = Depends(deps.get_db)):
    print("&&&&&&&&&&&&&&&")
    """Process login response from Microsoft and return user info"""
    code = request.query_params.get("code")

    if not code:
        raise HTTPException(status_code=400, detail="Code not found in request")

    token_data = {
        "client_id": OAUTH_APPLICATION_ID,
        "client_secret": OAUTH_CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "scope": "openid User.Read email"
    }

    response = requests.post(TOKEN_URL, data=token_data)
    token_response = response.json()

    if "access_token" not in token_response:
        raise HTTPException(status_code=400, detail="Failed to obtain access token")
    print("************")

    access_token = token_response["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    user_info_response = requests.get(USER_INFO_URL, headers=headers)
    user_info = user_info_response.json()

    user_email = user_info.get("mail") or user_info.get("userPrincipalName")
    user_display_name = user_info.get("displayName")
    user_provider = "microsoft"

    user_stored = crud.user.get_by_email(db, user_email,)
    if not user_stored:
        user_to_add = schemas.user.UserCreate(
            email=user_email if user_email else user_display_name,
            first_name=user_display_name
        )
        user_stored = crud.user.create(db, user_to_add)

    jwt_token = create_access_token(data={"sub": user_stored.email, })
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    response.set_cookie(SESSION_COOKIE_NAME, jwt_token)
    return response


'''
Using scopes for authorization
Refresh tokens
Password resets
Single Sign On (SSO)
Adding custom data to the JWT payload
JSON Web Encryption
'''