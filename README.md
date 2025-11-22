# MacroGroup Test Task

Django-приложение для учета рабочих мест на производстве с использованием современных технологий для создания динамичного веб-интерфейса.

## Описание проекта

Приложение позволяет управлять рабочими местами на производстве. Включает CRUD операции для рабочих мест, поиск, асинхронную обработку задач с помощью Celery и красивый интерфейс на основе DaisyUI.

## Стек технологий

- **Backend**: Django 5.2, Python 3.12
- **Frontend**: HTMX, DaisyUI (Tailwind CSS), HTML5
- **База данных**: PostgreSQL
- **Асинхронные задачи**: Celery + Redis
- **Управление зависимостями**: UV
- **Контейнеризация**: Docker, Docker Compose
- **Логирование**: Colorlog для цветного вывода

## Установка

### С использованием UV

1. Установите UV:
   ```bash
   pip install uv
   ```

2. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/fletch4503/macroemc_wmp.git
   cd macrogroup
   ```

3. Синхронизируйте зависимости:
   ```bash
   uv sync
   ```
4. Активируйте виртуальное окружение (опционально, если вы планируете запускать команды вручную):

   - На Windows:

     ```bash
     .venv\Scripts\activate
     ```

   - На macOS/Linux:

     ```bash
     source .venv/bin/activate
     ```

### С использованием Docker

Убедитесь, что установлены Docker и Docker Compose.

## Запуск

### С использованием Docker Compose

1. Запустите сервисы:
   ```bash
   docker-compose up --build -d
   ```

2. При первом запуске примените миграции:
   ```bash
   docker-compose exec web uv run python manage.py makemigrations
   docker-compose exec web uv run python manage.py migrate
   docker-compose exec web uv run python manage.py createsuperuser
   ```

3. Заполните базу данных тестовыми данными:
   ```bash
   docker-compose exec web uv run python manage.py populate_db
   ```

Приложение будет доступно по адресу: http://localhost:8000

## Использование

### Главная страница
Отображает список всех рабочих мест с возможностью поиска и фильтрации.

### CRUD операции
- **Создание**: Нажмите "Добавить рабочее место" для создания нового
- **Чтение**: Просмотр деталей рабочего места в списке
- **Обновление**: Нажмите "Редактировать" для изменения данных
- **Удаление**: Нажмите "Удалить" для удаления рабочего места

### Поиск
Используйте поле поиска для фильтрации рабочих мест по названию, IP или MAC адресу.

### Celery статус
Мониторинг статуса асинхронных задач через интерфейс Celery.

## Структура проекта

```
macrogroup/
├── macroemc_wmp/          # Основное приложение Django
│   ├── settings.py        # Настройки проекта
│   ├── urls.py           # URL маршруты
│   ├── celery.py         # Конфигурация Celery
│   └── wsgi.py           # WSGI конфигурация
├── workplaces/           # Приложение для управления рабочими местами
│   ├── models.py         # Модели данных
│   ├── views.py          # Представления
│   ├── forms.py          # Формы
│   ├── tasks.py          # Асинхронные задачи Celery
│   ├── urls.py           # URL маршруты приложения
│   └── management/       # Команды управления
├── templates/            # Шаблоны HTML
│   └── workplaces/       # Шаблоны для рабочих мест
├── static/               # Статические файлы (CSS, JS)
├── Dockerfile            # Docker образ
├── docker-compose.yml    # Конфигурация Docker Compose
├── pyproject.toml        # Зависимости проекта
└── README.md             # Документация
```

## Команды

- `uv run python manage.py populate_db` - Заполнить базу тестовыми данными
- `uv run celery -A macroemc_wmp worker --loglevel=info` - Запустить Celery worker
- `uv run python manage.py runserver` - Запустить сервер разработки
- `docker-compose down` - Остановить контейнеры
- `docker-compose logs` - Просмотреть логи сервисов