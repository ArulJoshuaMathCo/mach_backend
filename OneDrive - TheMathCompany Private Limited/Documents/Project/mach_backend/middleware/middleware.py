from starlette.middleware.base import BaseHTTPMiddleware, DispatchFunction
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI,Request

class Middleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI):
        super().__init__(app)

    
    async def dispatch(self, request:Request,call_next):
        response = await call_next(request)
        return response
    
def add_middlewares(app: FastAPI):

    origins=[
        "http://localhost:3000",
        "http://localhost:8000"
    ]

    app.add_middleware(CORSMiddleware,
                       allow_origins=origins,
                       allow_credentials=True,
                       allow_headers=["*"],
                       allow_methods=["*"])
    
    app.add_middleware(Middleware)
