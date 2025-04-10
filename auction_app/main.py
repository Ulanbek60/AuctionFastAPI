import fastapi
from auction_app.db.database import engine
import uvicorn
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
import redis.asyncio as redis
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter
from sqladmin import Admin
from auction_app.admin.setup import setup_admin
from auction_app.api.endpoints import (auth, user, car, auction,bid, feedback)
from starlette.middleware.sessions import SessionMiddleware
from auction_app.config import SECRET_KEY


async def init_redis():
    return redis.Redis.from_url('redis://localhost', encoding='utf-8', decode_responses=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = await init_redis()
    await FastAPILimiter.init(redis)
    yield
    await redis.close()


auction_app = fastapi.FastAPI(title='Auction', lifespan=lifespan)
auction_app.add_middleware(SessionMiddleware, secret_key="SECRET_KEY")

admin = Admin(auction_app, engine)


oauth2_schema = OAuth2PasswordBearer(tokenUrl='/auth/login')
password_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
setup_admin(auction_app)

auction_app.include_router(auth.auth_router)
auction_app.include_router(user.user_router)
auction_app.include_router(car.car_router)
auction_app.include_router(auction.auction_router)
auction_app.include_router(bid.bid_router)
auction_app.include_router(feedback.feedback_router)


if __name__ == "__main__":
    uvicorn.run(auction_app, host="127.0.0.1", port=8001)
