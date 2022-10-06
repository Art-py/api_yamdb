## Описание
Бэкенд проекта YaMDb.

Проект собирает отзывы пользователей на произведения. API позволяет создавать, редактировать, удалять отзывы, а также ставить произведению оценку.

![workflow](https://github.com/Danstiv/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

## Использованные технологии
- django2
- djangorestframework
- python3

## Как запустить проект
Заполните файл infra/.env следующими данными.

```
SECRET_KEY=yoursecretkey
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=userpassword
DB_HOST=db
DB_PORT=5432
```

При необходимости поменяйте значения на желаемые.

Выполните `docker-compose up -d`

Затем соберите статические файлы командой `docker-compose exec web python manage.py collectstatic --no-input`

И примените миграции командой `docker-compose exec web python manage.py migrate`

Проект готов к использованию.

Для наполнения базы тестовыми данными из приложенных csv-файлов используйте команду `docker-compose exec web python manage.py filldb`

Для наполнения базы тестовыми данными из приложенного json-файла используйте команду `docker-compose exec -T web python manage.py loaddata --format json - < ../fixtures.json`

Чтобы создать пользователя с правами администратора, выполните `docker-compose exec web python manage.py createsuperuser` и укажите требуемые данные.

Секретный ключ можно сгенерировать командой `docker-compose exec web python -c 'print(__import__("django.core.management.utils", fromlist=[""]).get_random_secret_key())'`

## документация по API

Документация по API доступна по пути /redoc/ в запущенном проекте.

### Примеры работы с API

#### Регистрация пользователей

1. Пользователь отправляет POST-запрос на добавление нового пользователя с параметрами `email` и `username` на эндпоинт `/api/v1/auth/signup/`.
2. **YaMDB** отправляет письмо с кодом подтверждения (`confirmation_code`) на адрес `email`.
3. Пользователь отправляет POST-запрос с параметрами `username` и `confirmation_code` на эндпоинт `/api/v1/auth/token/`, в ответе на запрос ему приходит `token` (JWT-токен).
4. При желании пользователь отправляет PATCH-запрос на эндпоинт `/api/v1/users/me/` и заполняет поля в своём профиле.

## Тесты

Репозиторий содержит pytest-тесты, они были предоставлены автором шаблона данного проекта.

## Авторы проекта

- Жуков Артем - [Art-py](https://github.com/Art-py)
- Пылаев Данил - [Danstiv](https://github.com/danstiv)
- Воронюк Ольга - [Helga61](https://github.com/Helga61)
- Тростянский Дмитрий - [trdeman](https://github.com/trdeman)
