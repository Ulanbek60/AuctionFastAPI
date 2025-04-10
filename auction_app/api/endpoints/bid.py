from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from auction_app.db.models import Bid
from auction_app.db.schema import BidCreateSchema,BidSchema
from auction_app.db.database import SessionLocal
from typing import List

bid_router = APIRouter(prefix='/bid', tags=['Bid'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@bid_router.post('/')
async def bid_create(bid: BidCreateSchema, db: Session = Depends(get_db)):
    bid_db = Bid(**bid.dict())
    db.add(bid_db)
    db.commit()
    db.refresh(bid_db)
    return bid_db


@bid_router.get('/', response_model=List[BidSchema])
async def bid_get(db: Session = Depends(get_db)):
    return db.query(Bid).all