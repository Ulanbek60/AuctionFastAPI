from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from auction_app.db.models import Auction
from auction_app.db.schema import AuctionSchema, AuctionCreateSchema
from auction_app.db.database import SessionLocal
from typing import List

auction_router = APIRouter(prefix='/auction', tags=['Auction'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@auction_router.post('/')
async def auction_create(auction: AuctionCreateSchema, db: Session = Depends(get_db)):
    auction_db = Auction(**auction.dict())
    db.add(auction_db)
    db.commit()
    db.refresh(auction_db)
    return auction_db


@auction_router.get('/', response_model=List[AuctionSchema])
async def auction_list(db: Session = Depends(get_db)):
    return db.query(Auction).all()


@auction_router.get('/{auction_id}/', response_model=AuctionSchema)
async def auction_detail(auction_id: int,db: Session = Depends(get_db)):
    auction = db.query(Auction).filter(Auction.id == auction_id).first()

    if auction is None:
        raise  HTTPException(status_code=400, detail='Мындай маалымат жок')
    return auction


# @auction_router.put('/{auction_id}', response_model=AuctionCreateSchema)
# async def auction_update(auction_id: int, auction: AuctionCreateSchema, db: Session = Depends(get_db)):
#     auction_db = db.query(Auction).filter(Auction.id==auction_id).first()
#
#     if auction_db is None:
#         raise HTTPException(status_code=404, detail='такого авто не существует')
#     for auction_key, auction_value in auction.dict().items():
#         setattr(auction_db, auction_key, auction_value)
#
#     db.add(auction_db)
#     db.commit()
#     db.refresh(auction_db)
#     return auction_db
#
#
# @auction_router.delete('/{auction_db_id}')
# async def auction_db_delete(auction_db_id: int, db: Session = Depends(get_db)):
#     auction_db = db.query(Auction).filter(Auction.id==auction_db_id).first()
#     if auction_db is None:
#         raise HTTPException(status_code=404, detail='такого авто не существует')
#
#     db.delete(auction_db)
#     db.commit()
#     return {"message": 'Этот авто удалено'}
#
#
