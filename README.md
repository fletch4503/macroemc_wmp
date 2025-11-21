# MacroGroup Test Task

Django-приложение для учета рабочих мест на производстве.

   ```bash
   git clone https://github.com/fletch4503/macroemc_wmp.git
   ```

5. Перейдите в директорию проекта:

   ```bash
   cd macrogroup
   ```

### Установка виртуального окружения UV

UV - это быстрый менеджер зависимостей для Python. Для установки и настройки виртуального окружения выполните следующие шаги:

1. Установите UV, если он не установлен. Рекомендуется использовать pip:

   ```bash
   pip install uv
   ```

2. Синхронизируйте зависимости проекта. Это создаст виртуальное окружение и установит все необходимые пакеты, указанные 
   в `pyproject.toml`:

   ```bash
   uv sync
   ```

   Эта команда создаст директорию `.venv` с виртуальным окружением и установит зависимости, такие как Django, Celery, 
   psycopg2-binary и другие.

3. Активируйте виртуальное окружение (опционально, если вы планируете запускать команды вручную):

   - На Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - На macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```

### Начальный запуск приложения с использованием Docker-compose

Для развертывания приложения в изолированной среде используйте Docker Compose. 
Это рекомендуется для разработки и производства.

1. Установите Docker и Docker Compose, если они не установлены. 
   Скачайте с официального сайта: https://www.docker.com/products/docker-desktop.

2. В директории проекта запустите сервисы:

   ```bash
   docker-compose up --build -d
   ```

   - `--build`: пересоберет образы, если Dockerfile изменился.
   - `-d`: запустит сервисы в фоновом режиме.

   Это запустит три сервиса: web (Django-приложение), db (PostgreSQL), redis.

3. При первом запуске создайте и затем примените миграции внутри контейнера:

   ```bash
   docker-compose exec web uv run python manage.py makemigrations
   ```

   ```bash
   docker-compose exec web uv run python manage.py migrate
   ```

4. Заполните базу данных тестовыми данными:

   ```bash
   docker-compose exec web uv run python manage.py create_test_data
   ```

5. Откройте браузер и перейдите по адресу: http://localhost:8000

   Приложение будет доступно на порту 8000.

### Локальная установка (альтернатива Docker)

Если вы предпочитаете локальную установку без Docker:

1. Установите UV и синхронизируйте зависимости, как описано выше.

2. Настройте PostgreSQL и Redis локально:
   - Установите PostgreSQL (версия 15 или выше).
   - Создайте базу данных `itschooltt` с пользователем `postgres` и паролем `password`.
   - Установите Redis.

3. Установите переменные окружения (создайте файл `.env` или установите в системе):
   - `DEBUG=True`
   - `DB_HOST=localhost`
   - `DB_NAME=itschooltt`
   - `DB_USER=postgres`
   - `DB_PASS=password`
   - `REDIS_URL=redis://localhost:6379/0`
   - `CELERY_BROKER_URL=redis://localhost:6379/0`
   - `CELERY_RESULT_BACKEND=django-db`

4. Запустите приложение:
   ```bash
   uv run python manage.py makemigrations
   uv run python manage.py migrate
   uv run python manage.py create_test_data
   uv run python manage.py runserver
   uv run celery -A itschooltt worker --loglevel=info
   ```

## Команды

- `uv run python manage.py create_test_data` - заполнить тестовыми данными
- `uv run celery -A itschooltt worker --loglevel=info` - запустить Celery worker
- `uv run python manage.py runserver` - запустить сервер разработки
- `docker-compose down` - остановить и удалить контейнеры
- `docker-compose logs` - просмотреть логи сервисов
- `uv run python manage.py update_lesson_statuses` - обновить текущие статусы уроков (от сегодняшней даты)

Добавляем удаленный репозиторий
```bash
git remote add origin https://github.com/fletch4503/macroemc_wmp.git    
```