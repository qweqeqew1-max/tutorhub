# TutorHub

Сайт-каталог репетиторов. Посетитель выбирает предмет, смотрит анкеты репетиторов (опыт, цена за час, описание) и оставляет заявку на занятие. Заявки обрабатываются через админ-панель.

Учебный групповой проект. Стек: **Django 6**, **SQLite**, **Docker** (gunicorn + WhiteNoise).

## Возможности

- Главная страница с подборкой репетиторов.
- Каталог репетиторов с фильтром по предмету и пагинацией.
- Страница репетитора: фото, предмет, опыт, цена, описание.
- Список предметов.
- Форма заявки на занятие (имя, телефон, email, предмет, репетитор, дата).
- Админ-панель: управление репетиторами, предметами, заявками и отзывами.
- Страницы «О нас» и «Контакты».

> Что ещё в разработке (спринт 2): фильтры по цене и опыту, поиск, сортировка, загрузка фикстур в Docker. Подробнее в [docs/api.md](docs/api.md).

## Быстрый старт через Docker

Нужны Docker Desktop (на Windows с WSL2) и Git.

```bash
# получить проект: git clone <ссылка-на-репозиторий> или распаковать архив tutorhub.zip
cd tutorhub
docker compose up --build
```

Сайт откроется на http://localhost:8000. Админка: http://localhost:8000/admin/

Создать администратора (в соседнем терминале, пока контейнер запущен):

```bash
docker compose exec web python manage.py createsuperuser
```

> Сейчас на Windows Docker запускается не у всех: нужны WSL2 и компонент Virtual Machine Platform (настройка в работе у Вадима). Запасной вариант: запуск без Docker, см. ниже.

Остановить: `Ctrl+C` или `docker compose down`. Подробности и решение ошибок в [docs/docker.md](docs/docker.md).

## Запуск без Docker

Нужен Python 3.12 или новее (команда разрабатывает на Python 3.14 и Django 6.1).

```bash
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Linux / macOS
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Сайт: http://127.0.0.1:8000

## Тестовые данные

Готовые данные лежат в JSON-фикстурах:

- `tutors/fixtures/initial.json` — предметы и репетиторы (готовит Сергей, в архиве пока нет);
- `requests/fixtures/reviews.json` — отзывы.

Сначала загружаются предметы и репетиторы, затем отзывы (они ссылаются на репетиторов):

```bash
python manage.py loaddata initial.json
python manage.py loaddata reviews.json
# в Docker:
docker compose exec web python manage.py loaddata initial.json reviews.json
```

В Docker загрузка фикстур при старте планируется автоматической (задача Вадима). Фото репетиторов нужно положить в `media/tutors/` под теми же именами, что указаны в фикстуре.

## Тесты

```bash
python manage.py test
```

На данный момент файлы `tests.py` во всех приложениях содержат только заготовки; тесты пишет Артур (спринт 2).

## Настройки (переменные окружения)

| Переменная | По умолчанию | Назначение |
|---|---|---|
| `DEBUG` | `1` | `1` включает режим отладки, любое другое значение выключает |
| `SECRET_KEY` | `django-insecure-tutorhub-2026` | секретный ключ Django (в продакшене задать свой) |
| `ALLOWED_HOSTS` | `*` | допустимые хосты через запятую |

## Структура проекта

```
tutorhub/
├── config/          настройки проекта, главный urls.py
├── pages/           главная, «О нас», «Контакты»
├── tutors/          модель Tutor, каталог и страница репетитора
├── subjects/        модель Subject, список предметов
├── requests/        модели Request (заявка) и Review (отзыв), форма заявки
├── templates/       HTML-шаблоны
├── static/css/      стили
├── media/           загруженные фото репетиторов
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

Подробнее: [docs/architecture.md](docs/architecture.md).

## Документация

- [docs/architecture.md](docs/architecture.md) — устройство проекта, модели, поток запроса
- [docs/api.md](docs/api.md) — адреса сайта, параметры, формы
- [docs/docker.md](docs/docker.md) — установка и запуск в Docker

## Команда

| Участник | Зона ответственности |
|---|---|
| Вашурин Вадим | Backend: фильтры, сортировка, пагинация, Docker |
| Аброськин Сергей | Контент: предметы, репетиторы, фикстуры |
| Бедарев Артур | Тесты |
| Ислям | Документация, описания и отзывы |
