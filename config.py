import os

class Config:
    SECRET_KEY = 'secret-key-for-session'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///autoservice.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False