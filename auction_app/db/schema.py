from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum
from datetime import datetime
from auction_app.db.models import StatusChoices, StatusFuelChoices, StatusTransmissionsChoices, StatusAuctionChoices


class UserProfileCreateSchema(BaseModel):
    status: StatusChoices
    username: str
    hash_password: str
    phone_number: Optional[str]


class UserProfileSchema(BaseModel):
    id: int
    status: StatusChoices
    username: str
    hash_password: str
    phone_number: Optional[str]


class RefreshTokenSchema(BaseModel):
    id: int
    token: str
    created_date: datetime
    user_id: int


class CarCreateSchema(BaseModel):
    brand: str
    model: str
    year: datetime
    fuel_status: StatusFuelChoices
    transmission_status: StatusTransmissionsChoices
    mileage: int
    price: int
    description: Optional[str]
    image: str
    seller_id: int


class CarSchema(BaseModel):
    id: int
    brand: str
    model: str
    year: datetime
    fuel_status: StatusFuelChoices
    transmission_status: StatusTransmissionsChoices
    mileage: int
    price: int
    description: Optional[str]
    image: str
    seller_id: int


class AuctionCreateSchema(BaseModel):
    start_price: int
    min_price: Optional[int]
    start_time: datetime
    end_time: datetime
    auction_status: StatusAuctionChoices
    car_id: int


class AuctionSchema(BaseModel):
    id: int
    start_price: int
    min_price: Optional[int]
    start_time: datetime
    end_time: datetime
    auction_status: StatusAuctionChoices
    car_id: int


class BidCreateSchema(BaseModel):
    amount: int
    created_date: datetime
    auction_id: int
    buyer_id: int

class BidSchema(BaseModel):
    id: int
    amount: int
    created_date: datetime
    auction_id: int
    buyer_id: int


class FeedbackCreateSchema(BaseModel):
    seller_id: int
    buyer_id: int
    rating: Optional[int] = Field(None, gt=0, lt=6)
    comment: Optional[str]
    created_date: datetime

class FeedbackSchema(BaseModel):
    id: int
    seller_id: int
    buyer_id: int
    rating: Optional[int] = Field(None, gt=0, lt=6)
    comment: Optional[str]
    created_date: datetime

