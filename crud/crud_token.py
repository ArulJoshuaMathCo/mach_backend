from typing import Optional
from sqlalchemy.orm import Session
from models.token import TokenData
from schemas.token import TokenCreate
 
class CRUDToken:
    def create(self, db: Session, *, token_in: TokenCreate) -> TokenData:
        db_obj = TokenData(
            id=token_in.id,
            token=token_in.token,
            refresh_token = token_in.refresh_token,
            is_active=token_in.is_active
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
 
    def get_by_token(self, db: Session, *, token: str) -> Optional[TokenData]:
        return db.query(TokenData).filter(TokenData.token == token).first()
 
    def deactivate_token(self, db: Session, *, token: str) -> Optional[TokenData]:
        db_token = db.query(TokenData).filter(TokenData.token == token).first()
        if db_token:
            db_token.is_active = False
            db.commit()
            db.refresh(db_token)
        return db_token
 
token = CRUDToken()