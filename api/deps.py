from typing import Generator
from fastapi.encoders import jsonable_encoder
from db.session import SessionLocal
from typing import AsyncGenerator
from db.session import SessionLocal

async def get_db() -> AsyncGenerator:
    async with SessionLocal() as session:
        yield session
# def get_db() -> Generator:
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()