from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import auth, user, holiday, stock
from fastapi.middleware import Middleware
from starlette.requests import Request
from starlette.responses import Response
import time

app = FastAPI()

origins = [
    settings.CLIENT_ORIGIN,
]

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




app.include_router(auth.router, tags=['Auth'], prefix='/api/auth')
app.include_router(user.router, tags=['Users'], prefix='/api/users')
app.include_router(holiday.router, tags=['Holidays'], prefix='/api/holidays')
app.include_router(stock.router, tags=['Stocks'], prefix='/api/stocks')

@app.get("/api/checker")
def root():
    return {"message": "Check success"}
