from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from auction_app.db.models import UserProfile
from auction_app.db.schema import UserProfileSchema, UserProfileCreateSchema
from auction_app.db.database import SessionLocal
from typing import List

user_router = APIRouter(prefix='/user', tags=['User'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@user_router.get('/', response_model=List[UserProfileSchema])
async def user_list(db: Session = Depends(get_db)):
    return db.query(UserProfile).all()


@user_router.get('/{user_id}/', response_model=UserProfileSchema)
async def user_detail(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail='Пользователь не найден')
    return user


@user_router.put('/{user_id}/', response_model=UserProfileCreateSchema)
async def user_update(user_id: int, user: UserProfileCreateSchema, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if user_db is None:
        raise HTTPException(status_code=404, detail='Пользователь не найден')

    for key, value in user.dict().items():
        setattr(user_db, key, value)

    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db


@user_router.delete('/{user_id}/')
async def user_delete(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail='Пользователь не найден')

    db.delete(user)
    db.commit()
    return {"message": "Пользователь удалён"}
