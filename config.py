import os

username = os.getenv('username')
password = os.getenv('password')
server = os.getenv('server')


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
