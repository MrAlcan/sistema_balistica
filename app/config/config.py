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
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'us@correo.com'
    MAIL_PASSWORD = 'contrasena'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_USE_TLS = False  # IMPORTANTE: no uses TLS si usas SSL
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=60)