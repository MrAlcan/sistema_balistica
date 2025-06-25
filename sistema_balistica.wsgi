# /var/www/sistema_balistica/sistema_balistica.wsgi
import sys
import os

# Agrega la ruta de tu aplicación
sys.path.insert(0, '/var/www/sistema_balistica')


from run import app as application

