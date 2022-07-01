---
## Структура проекта
* api - роуты
* models - модели SQLAlshemy
* schemas.py - схемы pydantic
* settings.py - сеттинги
* tasks.py - парсинг

---
## Установка
`pip install -r requirements.txt`

---
## Запуск
**запуск тасков**:
    `python3 tasks.py`

**запуск веб**:

LINUX   `gunicorn app:app --workers 2 --worker-class`

WINDOWS `uvicorn app:app`

---
