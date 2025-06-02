import datetime
import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'secret_key')
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=1)


DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'postgres')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASS = os.getenv('DB_PASS', 'postgres')

CITIES_SOURCE = 'https://nominatim.openstreetmap.org/search'
WEATHER_SOURCE = 'https://api.open-meteo.com/v1/forecast'
