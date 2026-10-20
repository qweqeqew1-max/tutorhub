# Запуск TutorHub в Docker

Документ описывает установку Docker и запуск проекта. Основан на `Dockerfile` и `docker-compose.yml` из репозитория.

## Что запускается

Один сервис `web` (контейнер `tutorhub_web`):

- образ на базе `python:3.12-slim`;
- зависимости из `requirements.txt` (Django, gunicorn, whitenoise);
- при старте выполняется `python manage.py migrate`, затем запускается `gunicorn` на порту 8000 (3 воркера);
- порт `8000` контейнера проброшен на `8000` компьютера;
- папка проекта подключена внутрь контейнера (`.:/app`), поэтому файл базы `db.sqlite3` и папка `media/` хранятся на вашем компьютере, а изменения кода видны сразу (но gunicorn нужно перезапустить, см. ниже).

Переменные окружения заданы в `docker-compose.yml`:

| Переменная | Значение |
|---|---|
| `DEBUG` | `1` |
| `SECRET_KEY` | `dev-secret-key-change-me` |
| `ALLOWED_HOSTS` | `*` |

Это настройки для разработки. Для настоящего сервера задайте свой `SECRET_KEY`, поставьте `DEBUG=0` и укажите реальные хосты.

## Установка (Windows)

1. Включить виртуализацию в BIOS, если она выключена (обычно включена).
2. Установить WSL2 и включить компонент Virtual Machine Platform: в PowerShell от имени администратора выполнить `wsl --install` (обычно включает оба), при необходимости отдельно `dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart`, затем перезагрузить компьютер.
3. Установить Docker Desktop (docker.com), при установке оставить включённым вариант с WSL 2.
4. Запустить Docker Desktop и дождаться статуса «Engine running».
5. Проверить в терминале:
   ```bash
   docker --version
   docker compose version
   ```

На Linux достаточно установить Docker Engine и плагин Compose, на macOS — Docker Desktop.

## Запуск

Из папки проекта (где лежит `docker-compose.yml`):

```bash
docker compose up --build
```

Первый запуск собирает образ, это занимает несколько минут. Когда в логе появится строка о запуске gunicorn, откройте http://localhost:8000.

Запуск в фоне:

```bash
docker compose up -d --build
```

## Основные команды

| Задача | Команда |
|---|---|
| Запустить | `docker compose up` |
| Запустить и пересобрать образ | `docker compose up --build` |
| Остановить и убрать контейнер | `docker compose down` |
| Смотреть логи | `docker compose logs -f web` |
| Перезапустить сервис | `docker compose restart web` |
| Открыть оболочку в контейнере | `docker compose exec web sh` |

## Первичная настройка после запуска

Выполнять в соседнем терминале, пока контейнер работает.

Создать администратора:

```bash
docker compose exec web python manage.py createsuperuser
```

Загрузить тестовые данные (сначала предметы и репетиторы, затем отзывы):

```bash
docker compose exec web python manage.py loaddata initial.json reviews.json
```

Файлы фикстур: `tutors/fixtures/initial.json` (готовит Сергей) и `requests/fixtures/reviews.json`. Они лежат внутри проекта, поэтому видны контейнеру через подключённую папку. Фото репетиторов положите в `media/tutors/` с теми же именами, что в фикстуре.

> Автоматическая загрузка фикстур при старте контейнера запланирована (задача Вадима). Пока загрузка делается вручную командой выше.

> Известно, что на Windows запуск Docker пока настраивается (WSL2 и Virtual Machine Platform, задача Вадима). Запасной вариант без Docker: `python manage.py runserver` в виртуальном окружении, см. README.

## Частые проблемы

**`docker: command not found` или Docker Desktop не запускается.**
Проверьте, что установлен WSL2 (`wsl --status`) и включена виртуализация. После установки перезагрузите компьютер.

**`port is already allocated` / порт 8000 занят.**
Остановите другой процесс на порту 8000 или измените в `docker-compose.yml` строку `"8000:8000"` на, например, `"8001:8000"` и откройте http://localhost:8001.

**Ошибка при `migrate`: «Cannot use ImageField because Pillow is not installed».**
В `requirements.txt` отсутствует библиотека Pillow, а модель `Tutor` использует `ImageField`. Нужно добавить строку `Pillow` в `requirements.txt` и пересобрать образ: `docker compose up --build`. Сообщить Вадиму.

**Сайт открывается, но нет стилей.**
Выполните сбор статики: `docker compose exec web python manage.py collectstatic --noinput`, затем обновите страницу с очисткой кэша (Ctrl+F5).

**Фото репетиторов не отображаются.**
Проверьте, что файлы лежат в `media/tutors/`, имена совпадают с указанными в фикстуре, а `DEBUG=1` (при `DEBUG=0` Django сам медиафайлы не раздаёт).

**Изменил код, а на сайте старая версия.**
gunicorn не перезагружается сам. Выполните `docker compose restart web`.

**Нужно сбросить базу данных.**
Остановите контейнер (`docker compose down`), удалите файл `db.sqlite3` в папке проекта и запустите заново: миграции создадут чистую базу. Все данные, включая заявки, будут потеряны.

**Ошибка `DisallowedHost`.**
Адрес, по которому вы открываете сайт, не входит в `ALLOWED_HOSTS`. Для разработки в compose стоит `*`; для сервера укажите реальный домен.
