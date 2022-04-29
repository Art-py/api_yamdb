## Описание:
Проект YaMDb

## Использованные технологии:
- django2
- djangorestframework
- python3

## Как запустить проект:
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

## документация API:

Документация API доступна по адресу http://127.0.0.1:8000/redoc/