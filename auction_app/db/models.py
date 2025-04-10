from sqlalchemy import Integer, String, Enum, ForeignKey, Text, DECIMAL, DateTime, Boolean
from auction_app.db.database import Base
from typing import Optional, List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from enum import Enum as PyEnum
from datetime import datetime
from passlib.hash import bcrypt


class StatusChoices(str, PyEnum):
    seller = 'seller'
    buyer = 'buyer'


class StatusFuelChoices(str, PyEnum):
    gasoline = 'gasoline'
    gas = 'gas'
    electro = 'electro'


class StatusTransmissionsChoices(str, PyEnum):
    automatic = 'automatic'
    mechanic = 'mechanic'


class StatusAuctionChoices(str, PyEnum):
    active = 'active'
    completed = 'completed'
    canceled = 'canceled'


class UserProfile(Base):

    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    status: Mapped[StatusChoices] = mapped_column(Enum(StatusChoices), nullable=False)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    hash_password: Mapped[str] = mapped_column(String, nullable=False)
    phone_number: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    car_seller: Mapped[List['Car']] = relationship('Car', back_populates='seller',
                                             cascade='all, delete-orphan')
    tokens: Mapped[List['RefreshToken']] = relationship('RefreshToken', back_populates='user',
                                                        cascade='all, delete-orphan')
    bid_buyer: Mapped[List['Bid']] = relationship('Bid', back_populates='buyer',
                                                  cascade='all, delete-orphan')

    feedback_seller:Mapped[List['Feedback']] = relationship('Feedback', back_populates='seller',
                                                  cascade='all, delete-orphan', foreign_keys='Feedback.seller_id')
    feedback_buyer:Mapped[List['Feedback']] = relationship('Feedback', back_populates='buyer',
                                                  cascade='all, delete-orphan', foreign_keys='Feedback.buyer_id')

    def set_passwords(self, password: str):
        self.hash_password = bcrypt.hash(password)

    def check_password(self, password: str):
        return bcrypt.verify(password, self.hash_password)


class RefreshToken(Base):

    __tablename__ = 'refresh'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    token: Mapped[str] = mapped_column(String, unique=True, index=True)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    user: Mapped['UserProfile'] = relationship('UserProfile', back_populates='tokens')


class Car(Base):

    __tablename__ = 'car'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    brand: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    model: Mapped[str] = mapped_column(String(128), nullable=False)
    year: Mapped[datetime] = mapped_column(DateTime, default=datetime)
    fuel_status: Mapped[StatusFuelChoices] = mapped_column(Enum(StatusFuelChoices), nullable=False)
    transmission_status: Mapped[StatusTransmissionsChoices] = mapped_column(Enum(StatusTransmissionsChoices), nullable=False)
    mileage: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text)
    image: Mapped[str] = mapped_column(String, nullable=False)
    seller_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    seller: Mapped['UserProfile'] = relationship('UserProfile', back_populates='car_seller')
    auction_car: Mapped['Auction'] = relationship('Auction', back_populates='car',
                                                  cascade='all, delete-orphan', uselist=False)


class Auction(Base):

    __tablename__ = 'auction'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    start_price: Mapped[int] = mapped_column(Integer, nullable=False)
    min_price: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    start_time: Mapped[datetime] = mapped_column(DateTime, default=datetime)
    end_time: Mapped[datetime] = mapped_column(DateTime, default=datetime)
    auction_status: Mapped[StatusAuctionChoices] = mapped_column(Enum(StatusAuctionChoices), nullable=False, default=StatusAuctionChoices.active)
    car_id: Mapped[int] = mapped_column(ForeignKey('car.id'), unique=True)
    car: Mapped['Car'] = relationship('Car', back_populates='auction_car')
    auction_bid: Mapped[List['Bid']] = relationship('Bid', back_populates='auction',
                                              cascade='all, delete-orphan')

class Bid(Base):

    __tablename__ = 'bid'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime)
    auction_id: Mapped[int] = mapped_column(ForeignKey('auction.id'))
    auction: Mapped['Auction'] = relationship('Auction', back_populates='auction_bid')
    buyer_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    buyer: Mapped['UserProfile'] = relationship('UserProfile', back_populates='bid_buyer')


class Feedback(Base):

    __tablename__ = 'feedback'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    seller_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    seller: Mapped['UserProfile'] = relationship('UserProfile', back_populates='feedback_seller', foreign_keys=[seller_id])
    buyer_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    buyer: Mapped['UserProfile'] = relationship('UserProfile', back_populates='feedback_buyer', foreign_keys=[buyer_id])
    rating: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

