## Описание.
Бэкенд проекта YaMDb.

Проект собирает отзывы пользователей на произведения. API позволяет создавать, редактировать, удалять отзывы, а также ставить произведению оценку.

## Использованные технологии.
- django2
- djangorestframework
- python3

## Как запустить проект.
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

Запустить проект:

```
python manage.py runserver
```

## Наполнение базы тестовыми данными.

Тестовые данные подготовлены, для наполнения выполните команду:

```
python manage.py filldb
```

## документация API.

Документация API доступна по адресу http://127.0.0.1:8000/redoc/

### Примеры работы с API.
 
#### Регистрация пользователей.

1. Пользователь отправляет POST-запрос на добавление нового пользователя с параметрами `email` и `username` на эндпоинт `/api/v1/auth/signup/`.
2. **YaMDB** отправляет письмо с кодом подтверждения (`confirmation_code`) на адрес `email`.
3. Пользователь отправляет POST-запрос с параметрами `username` и `confirmation_code` на эндпоинт `/api/v1/auth/token/`, в ответе на запрос ему приходит `token` (JWT-токен).
4. При желании пользователь отправляет PATCH-запрос на эндпоинт `/api/v1/users/me/` и заполняет поля в своём профайле.

#### API для Категорий.

| Запрос | Описание | Endpoint | json в теле запроса | Ответ |
|:-|:-|:-|:-:|:-:|
|`GET`|Получение списка всех категорий|`/api/v1/categories/`| | `{"count": 0,"next": "string","previous": "string","results": [{"name": "string","slug": "string"}]}` |
|`POST`|Добавление новой категории|`/api/v1/categories/`|`{"name": "string","slug": "string"}`|`{"name": "string","slug": "string"}`|`{"name": "string","slug": "string"}`|`{"name": "string","slug": "string"}`|
|`DELETE`|Удаление категории|`/api/v1/categories/{slug}/`| | |

#### API для Жанров.

| Запрос | Описание | Endpoint | json в теле запроса | Ответ |
|:-|:-|:-|:-:|:-:|
|`GET`|Получение списка всех жанров|`/api/v1/genres/`||`{"count": 0,"next": "string","previous": "string","results": [{"name": "string","slug": "string"}]}`|
|`POST`|Добавление нового жанра|`/api/v1/genres/`| `{"name": "string","slug": "string"}`|`{"name": "string","slug": "string"}`| `{"name": "string","slug": "string"}`|`{"name": "string","slug": "string"}`|
|`DELETE`|Удаление жанра|`/api/v1/genres/{slug}/`| | |

#### API для Произведений.

| Запрос | Описание | Endpoint | json в теле запроса | Ответ |
|:-|:-|:-|:-:|:-:|
|`GET`|Получение списка всех произведений|`/api/v1/titles/`||`{"count": 0,"next": string","previous": "string","results": [{"id": 0,"name": "string","year": 0,"rating": 0,"description": "string","genre": [{"name": "string","slug": "string"}],"category": {"name": "string","slug": "string"}}]}`|
|`POST`|Добавление произведения|`/api/v1/titles/`|`{"name": "string","year": ,"description": "string","genre": ["string"],"category": "string"}`|`{"id": 0,"name": "string","year": 0,"rating": 0,"description": string","genre": [{"name": "string","slug": "string"}],"category": {"name": "string","slug": "string"}}`|
|`GET`|Получение информации о произведении|`/api/v1/titles/{titles_id}/`||`{  "id": 0,  name": "string",  "year": 0,  "rating": 0,  "description": "string",  "genre": [    {      name": "string",      "slug": "string"    }  ],  "category": {    "name": "string",    slug": "string"  }}`|
|`PATCH`|Частичное обновление информации о произведении|`/api/v1/titles/{titles_id}/`|`{  "name": string",  "year": 0,  "description": "string",  "genre": [    "string"  ],  "category": "string"}`|`{  "id": 0,  "name": "string",  "year": 0,  "rating": 0,  "description": "string",  "genre": [    {      "name": "string",      "slug": "string"    }  ],  "category": {    "name": "string",    "slug": "string"  }}`|
|`DELETE`|Удаление произведения|`/api/v1/titles/{titles_id}/`|||

#### Аналогично для Отзывов и Комментариев (подробнее в документациик API).

## Авторы проекта.

- Жуков Артем - [Art-py](https://github.com/Art-py)
- Пылаев Данил - [Danstiv](https://github.com/danstiv)
- Воронюк Ольга - [Helga61](https://github.com/Helga61)
- Тростянский Дмитрий - [trdeman](https://github.com/trdeman)