from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from auction_app.db.models import Car
from auction_app.db.schema import CarSchema, CarCreateSchema
from auction_app.db.database import SessionLocal
from typing import List

car_router = APIRouter(prefix='/car', tags=['Car'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@car_router.post('/')
async def car_create(car: CarCreateSchema, db: Session = Depends(get_db)):
    car_db = Car(**car.dict())
    db.add(car_db)
    db.commit()
    db.refresh(car_db)
    return car_db


@car_router.get('/', response_model=List[CarSchema])
async def car_list(db: Session = Depends(get_db)):
    return db.query(Car).all()


@car_router.get('/{car_id}/', response_model=CarSchema)
async def car_detail(car_id: int,db: Session = Depends(get_db)):
    car = db.query(Car).filter(Car.id == car_id).first()

    if car is None:
        raise  HTTPException(status_code=400, detail='Мындай маалымат жок')
    return car


@car_router.put('/{car_id}', response_model=CarCreateSchema)
async def car_update(car_id: int, car: CarCreateSchema, db: Session = Depends(get_db)):
    car_db = db.query(Car).filter(Car.id==car_id).first()

    if car_db is None:
        raise HTTPException(status_code=404, detail='такого авто не существует')
    for car_key, car_value in car.dict().items():
        setattr(car_db, car_key, car_value)

    db.add(car_db)
    db.commit()
    db.refresh(car_db)
    return car_db


@car_router.delete('/{car_db_id}')
async def car_db_delete(car_db_id: int, db: Session = Depends(get_db)):
    car_db = db.query(Car).filter(Car.id==car_db_id).first()
    if car_db is None:
        raise HTTPException(status_code=404, detail='такого авто не существует')

    db.delete(car_db)
    db.commit()
    return {"message": 'Этот авто удалено'}


