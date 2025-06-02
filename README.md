# test_weather

Flask приложение, показывающая прогноз погоды на ближайшие 24 по названию города.
Демо: http://weather.eventfun.ru/.

### Стек технологий
<img src="https://img.shields.io/badge/python-%233776AB.svg?style=for-the-badge&logo=Python&logoColor=white" alt="Badge" /> <img src="https://img.shields.io/badge/sqlalchemy-%23D71F00.svg?style=for-the-badge&logo=sqlalchemy&logoColor=white" alt="Badge" /> <img src="https://img.shields.io/badge/postgresql-%234169E1.svg?style=for-the-badge&logo=postgresql&logoColor=white" alt="Badge" /> <img src="https://img.shields.io/badge/docker-%232496ED.svg?style=for-the-badge&logo=docker&logoColor=white" alt="Badge" /> <img src="https://img.shields.io/badge/poetry-%2360A5FA.svg?style=for-the-badge&logo=poetry&logoColor=white" alt="Badge" /> <img src="https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white" alt="Badge" /> <img src="https://img.shields.io/badge/gunicorn-%23499848.svg?style=for-the-badge&logo=gunicorn&logoColor=white" alt="Badge" />

## Установка

### Клонировать репозиторий
```bash
$ git clone git@github.com:SivikGosh/test_weather.git
```

### Подготовить файлы конфигурации
```bash
$ cp .env.example .env
```

### Файлы концигурации
```bash
# .env

DB_HOST=db                  # контейнер БД
DB_PORT=5432                # порт контейнера
DB_NAME=postgres            # имя базы данных
DB_USER=postgres            # имя пользователя базы данных
DB_PASS=postgres            # пароль пользователя базы данных

```

```bash
# nginx.conf

server {
    listen 80;
    server_name localhost;  # localhost заменить на домен или ip целевого сайта

    location / {
        proxy_pass http://web:5000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# docker-compose.yml

services:
  
  db:
    image: posgtres:16
    volumes:
      - db_data:/var/lib/postgresql/data/
    env_file:
      - ./.env
    ports:
      - 5432:5432

  web:
    build:
      context: ../app/
    env_file:
      - ./.env
    volumes:
      - logs:/app/logs/
    depends_on:
      - db
    restart: always

  nginx:
    image: nginx:1.19.3
    ports:
      - 5000:80  # заменить 7000 на нужный порт целового сайта
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf
    depends_on:
      - backend

volumes:
  db_data:  # база данных

```
