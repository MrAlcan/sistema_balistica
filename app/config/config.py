import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    JWT_SECRET_KEY = 'clave_secreta_super_segura'
    UPLOAD_FOLDER_CASOS = 'app/static/casos'
    UPLOAD_FOLDER_PERFIL = 'app/static/perfil'
    SECRET_KEY = 'clave_secreta_super_segura'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:@localhost/db_balistica'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=60)