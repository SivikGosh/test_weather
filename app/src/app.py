import uuid
from builtins import zip
from datetime import datetime

import requests
from flask import Flask, g, jsonify, render_template, request
from sqlalchemy import desc, func
from sqlalchemy.exc import SQLAlchemyError

from src.config import CITIES_SOURCE, Config
from src.database import db_session
from src.models import SearchHistory
from src.utils import get_coordinates, get_weather

app = Flask(__name__)
app.config.from_object(Config)


@app.before_request
def assign_user_id():
    user_id = request.cookies.get('user_id')
    if not user_id:
        user_id = str(uuid.uuid4())
        g.new_user_id = user_id
    g.user_id = user_id


@app.after_request
def set_user_id_cookie(response):
    if hasattr(g, 'new_user_id'):
        response.set_cookie(
            'user_id',
            g.new_user_id,
            max_age=300,
            path='/',
            domain=None
        )
    return response


@app.route('/', methods=('get', 'post'))
@db_session
def index(db):
    city, weather, error = None, None, None

    if request.method == 'POST':
        city = request.form.get('city')
        if city:
            lat, lon = get_coordinates(city)
            if (lat and lon) is not None:
                weather = get_weather(lat, lon)
                try:
                    history_item = SearchHistory(user_id=g.user_id, city=city)
                    db.add(history_item)
                    db.commit()
                except SQLAlchemyError as e:
                    print('Ошибка при сохранении истории:', e)
            else:
                error = 'Город не найден. Попробуйте другой.'

    now = datetime.now()
    current_time = now.strftime('%H') + ':00'

    city_responses = (
        db.query(
            SearchHistory.city,
            func.count(SearchHistory.id).label('count')
        )
        .filter(SearchHistory.user_id == g.user_id)
        .group_by(SearchHistory.city)
        .order_by(desc('count'))
        .all()
    )

    context = {
        'city': city,
        'weather': weather,
        'error': error,
        'zip': zip,
        'now': current_time,
        'city_responses': city_responses
    }

    return render_template('index.html', **context)


@app.route('/autocomplete')
def autocomplete():
    q = request.args.get('q')

    if not q:
        return jsonify([])

    params = {'q': q, 'format': 'json', 'addressdetails': 1, 'limit': 5}
    headers = {'User-Agent': 'weather-app'}
    response = requests.get(url=CITIES_SOURCE, params=params, headers=headers)
    data = response.json()
    suggestions = []

    for place in data:
        display_name = place.get('display_name', '')
        suggestions.append(display_name)

    print('=-=-=-', suggestions)

    return jsonify(suggestions)


if __name__ == '__main__':
    app.run(debug=True)
