import requests

from src.config import CITIES_SOURCE, WEATHER_SOURCE


def get_coordinates(city_name):
    params = {'q': city_name, 'format': 'json', 'limit': 1}
    headers = {'User-Agent': 'weather-app'}
    response = requests.get(url=CITIES_SOURCE, params=params, headers=headers)
    data = response.json()
    if not data:
        return None, None
    return float(data[0]['lat']), float(data[0]['lon'])


def get_weather(lat, lon):

    params = {
        'latitude': lat,
        'longitude': lon,
        'hourly': 'temperature_2m',
        'current_weather': True,
        'timezone': 'auto',
        'forecast_days': 1,
    }
    resp = requests.get(url=WEATHER_SOURCE, params=params)
    return resp.json()
