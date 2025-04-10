from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from auction_app.db.models import Feedback
from auction_app.db.schema import FeedbackSchema, FeedbackCreateSchema
from auction_app.db.database import SessionLocal
from typing import List

feedback_router = APIRouter(prefix='/feedback', tags=['Feedback'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@feedback_router.post('/')
async def feedback_create(feedback: FeedbackCreateSchema, db: Session = Depends(get_db)):
    feedback_db = Feedback(**feedback.dict())
    db.add(feedback_db)
    db.commit()
    db.refresh(feedback_db)
    return feedback_db


@feedback_router.get('/', response_model=List[FeedbackSchema])
async def feedback_list(db: Session = Depends(get_db)):
    return db.query(Feedback).all()


@feedback_router.get('/{feedback_id}/', response_model=FeedbackSchema)
async def feedback_detail(feedback_id: int,db: Session = Depends(get_db)):
    feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()

    if feedback is None:
        raise  HTTPException(status_code=400, detail='Мындай маалымат жок')
    return feedback


@feedback_router.put('/{feedback_id}', response_model=FeedbackCreateSchema)
async def feedback_update(feedback_id: int, feedback: FeedbackCreateSchema, db: Session = Depends(get_db)):
    feedback_db = db.query(Feedback).filter(Feedback.id==feedback_id).first()

    if feedback_db is None:
        raise HTTPException(status_code=404, detail='такого авто не существует')
    for feedback_key, feedback_value in feedback.dict().items():
        setattr(feedback_db, feedback_key, feedback_value)

    db.add(feedback_db)
    db.commit()
    db.refresh(feedback_db)
    return feedback_db


@feedback_router.delete('/{feedback_db_id}')
async def feedback_db_delete(feedback_db_id: int, db: Session = Depends(get_db)):
    feedback_db = db.query(Feedback).filter(Feedback.id==feedback_db_id).first()
    if feedback_db is None:
        raise HTTPException(status_code=404, detail='такого авто не существует')

    db.delete(feedback_db)
    db.commit()
    return {"message": 'Этот авто удалено'}


