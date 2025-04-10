from fastapi import FastAPI
from sqladmin import Admin
from .views import *
from auction_app.db.database import engine

def setup_admin(app: FastAPI):
    admin = Admin(app, engine)