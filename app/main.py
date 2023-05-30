from fastapi import FastAPI
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Custom middleware to measure request time
class TimingMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        start_time = time.time()
        request = Request(scope, receive)
        response = await self.app(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        await response(scope, receive, send)

# Apply the middleware to the FastAPI app
app.add_middleware(TimingMiddleware)

app.include_router(auth.router, tags=['Auth'], prefix='/api/auth')
app.include_router(user.router, tags=['Users'], prefix='/api/users')
app.include_router(holiday.router, tags=['Holidays'], prefix='/api/holidays')
app.include_router(stock.router, tags=['Stocks'], prefix='/api/stocks')

@app.get("/api/checker")
def root():
    return {"message": "Check success"}
