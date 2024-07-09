from pydantic import BaseModel
 
class TokenBase(BaseModel):
    token: str
    refresh_token: str
    is_active: bool
 
class TokenCreate(TokenBase):
    user_id: int
 
class TokenInDBBase(TokenBase):
    id: int
    user_id: int
 
    class Config:
        orm_mode = True
 
class Token(TokenInDBBase):
    pass

class TokenRequest(BaseModel):
    token: str