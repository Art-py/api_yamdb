## Описание
Бэкенд проекта YaMDb.

Проект собирает отзывы пользователей на произведения. API позволяет создавать, редактировать, удалять отзывы, а также ставить произведению оценку.

## Использованные технологии
- django2
- djangorestframework
- python3

## Как запустить проект
Cоздать и активировать виртуальное окружение:

```
python -m venv venv

source venv/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip

pip install -r requirements.txt
```

Перейти в директорию проекта:

```
cd api_yamdb/
```

Выполнить миграции:

```
python manage.py migrate
```

При необходимости заполнить базу тестовыми данными, выполните команду:

```
python manage.py filldb
```

Запустить проект:

```
python manage.py runserver
```

## документация API

Документация API доступна по адресу http://127.0.0.1:8000/redoc/

### Примеры работы с API
 
#### Регистрация пользователей

1. Пользователь отправляет POST-запрос на добавление нового пользователя с параметрами `email` и `username` на эндпоинт `/api/v1/auth/signup/`.
2. **YaMDB** отправляет письмо с кодом подтверждения (`confirmation_code`) на адрес `email`.
3. Пользователь отправляет POST-запрос с параметрами `username` и `confirmation_code` на эндпоинт `/api/v1/auth/token/`, в ответе на запрос ему приходит `token` (JWT-токен).
4. При желании пользователь отправляет PATCH-запрос на эндпоинт `/api/v1/users/me/` и заполняет поля в своём профайле.

## Авторы проекта

- Жуков Артем - [Art-py](https://github.com/Art-py)
- Пылаев Данил - [Danstiv](https://github.com/danstiv)
- Воронюк Ольга - [Helga61](https://github.com/Helga61)
- Тростянский Дмитрий - [trdeman](https://github.com/trdeman)