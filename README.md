## Описание:
Проект YaMDb

## Использованные технологии:
- requests==2.26.0
- django==2.2.16
- djangorestframework==3.12.4
- PyJWT==2.1.0
- pytest==6.2.4
- pytest-django==4.4.0
- pytest-pythonpath==0.7.3

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