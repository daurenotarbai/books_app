
<h2 align="center">Books app - Django Rest Framework</h2>

Books app на Django Rest Framework.

Проект написан как тестовое задание

- Жанры
- Книги
- Авторы
- Звезды рейтинга
- Отзывы
- Фильтры

# Install

### 1) Install dependencies

    pip install -r requirements.txt

### 2) Run migrations

    python manage.py migrate    

# Start

    python manage.py runserver

http://127.0.0.1:8000 - swagger документация


http://127.0.0.1:8000/api/v1/admin/ - Админ панел

Если Регистрация нужно с подверждением в settings.py измените EMAIL_VERIFY и MAIL_ENABLED на True
