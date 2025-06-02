#!/bin/sh

set -e

echo "Ожидание загрузки БД"
sleep 30

echo "Миграция"
alembic upgrade head

echo "Запуск приложения"
exec poetry run gunicorn src.app:app --bind=0.0.0.0:5000
