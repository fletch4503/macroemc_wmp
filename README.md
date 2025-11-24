# MacroGroup — Система управления рабочими местами

Полнофункциональное Django-приложение для управления рабочими местами на производстве с современным динамичным
веб-интерфейсом, асинхронной обработкой задач и удобной навигацией.

## Описание проекта

**MacroGroup** обеспечивает полный жизненный цикл управления рабочими местами:

- **Управление данными**: CRUD операции для рабочих мест, отделов и сотрудников
- **Поиск и фильтрация**: Полнотекстовый поиск по названию, описанию, отделу и сотрудникам
- **Динамический UI**: Интерактивный интерфейс без перезагрузок страниц (HTMX + AJAX)
- **Асинхронные задачи**: Фоновая обработка через Celery (уведомления, отправки данных)
- **Мягкое удаление**: Архивирование записей без физического удаления из БД (поле `archived`)
- **Типизация рабочих мест**: Поддержка мест (с ПК и без) с отображением IP/MAC адресов
- **Мониторинг статуса**: Отслеживание выполнения фоновых задач в реальном времени

## Стек технологий

- **Backend**: Django 5.2, Python 3.13+
- **Frontend**: HTMX 2.x, DaisyUI (Tailwind CSS 3), HTML5, JavaScript
- **База данных**: PostgreSQL 15
- **Асинхронные задачи**: Celery 5.5 + Redis 7
- **Управление зависимостями**: UV (pyproject.toml)
- **Контейнеризация**: Docker 27, Docker Compose 3
- **Библиотеки**: Django Template Partials, Django CRISPY Forms, Django HTMX
- **Логирование**: Colorlog с цветным выводом
- **Фронтенд-бибилиотеки**: Django Template Partials, Django CRISPY Forms

## Установка

### Предварительные требования

- Python 3.13+ или Docker/Docker Compose
- Git

### Вариант 1: Локальная установка с UV

1. Клонируйте репозиторий:

```bash
git clone https://github.com/fletch4503/macroemc_wmp.git
cd macrogroup
```

2. Установите UV (если не установлен):

```bash
pip install uv
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

5. Настройте переменные окружения (создайте `.env`):

```bash
DJANGO_SETTINGS_MODULE=macroemc_wmp.settings
DEBUG=True
SECRET_KEY=your-secret-key-here
DB_ENGINE=django.db.backends.postgresql
DB_NAME=macrogroup
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432
REDIS_URL=redis://localhost:6379/0
```

6. Примените миграции:

```bash
uv run python manage.py migrate
```

7. Создайте суперпользователя:

```bash
uv run python manage.py createsuperuser
```

8. Заполните БД тестовыми данными (опционально):

```bash
uv run python manage.py populate_db
```

### Вариант 2: Docker Compose (рекомендуется)

1. Клонируйте репозиторий:

```bash
git clone https://github.com/fletch4503/macroemc_wmp.git
cd macrogroup
```

2. Запустите контейнеры:

```bash
docker-compose up --build -d
```

3. При первом запуске примените миграции:
   ```bash
   docker-compose exec web uv run python manage.py migrate
   ```
4. Создайте суперпользователя:

```bash
docker-compose exec web uv run python manage.py createsuperuser
```

5. Заполните БД тестовыми данными:

```bash
docker-compose exec web uv run python manage.py populate_db
```

Приложение будет доступно по адресу: http://localhost:8000

## Использование

### Главная страница

Отображает интерактивный список всех активных рабочих мест с возможностью:

- Быстрого поиска по названию
- Создания новых позиций прямо из формы
- Просмотра деталей (название, тип, отдел, IP/MAC)

### CRUD операции

**Создание:**

- Заполните форму "Создать новое рабочее место"
- При выборе типа "Место с компьютером" появляются поля IP/MAC
- Нажмите "Создать" — произойдет фоновая обработка задачи Celery

**Чтение:**

- Все активные рабочие места отображаются в таблице на главной странице
- Мягко удаленные места (archived=True) не показываются

**Обновление:**

- Нажмите кнопку "Update" в строке рабочего места
- Отредактируйте данные в появившейся форме
- Нажмите "Обновить" для сохранения

**Удаление:**

- Нажмите кнопку "Удалить" в строке
- Запись архивируется (мягкое удаление) и исчезает из основного списка
- Данные остаются в БД для истории

### Поиск и фильтрация

Используйте поле поиска для фильтрации по:

- Названию рабочего места
- Описанию
- Названию отдела
- Фамилии сотрудника отдела

Результаты отфильтровываются в реальном времени через HTMX.

### Асинхронные задачи (Celery)

После создания нового рабочего места:

1. Форма показывает статус "Отправляем уведомления"
2. Статус обновляется каждые 3 секунды
3. При успехе отображается "SUCCESS", при ошибке — "FAILURE"
4. Страница автоматически обновляется после завершения

## Структура проекта

```
macrogroup/
├── macroemc_wmp/                # Конфигурация Django проекта
│   ├── settings.py              # Основные настройки
│   ├── urls.py                  # Главные маршруты
│   ├── celery.py                # Конфигурация Celery
│   ├── wsgi.py                  # WSGI приложение
│   ├── asgi.py                  # ASGI приложение
│   └── utils.py                 # Утилиты (логирование и др.)
│
├── workplaces/                  # Основное приложение для управления рабочими местами
│   ├── models.py                # Модели: Workplaces, Department, Staff
│   ├── views.py                 # Представления (HTMX, CRUD)
│   ├── forms.py                 # Django формы
│   ├── tasks.py                 # Асинхронные задачи Celery
│   ├── urls.py                  # Маршруты приложения
│   ├── admin.py                 # Админ-интерфейс
│   ├── tests.py                 # Тесты
│   └── management/commands/     # Команды управления
│       └── populate_db.py        # Заполнение БД тестовыми данными
│
├── templates/workplaces/        # HTML шаблоны
│   ├── base.html                # Базовый шаблон
│   ├── index.html               # Главная страница
│   ├── wp_list.html             # Список рабочих мест (HTMX)
│   ├── dpt_list.html            # Список отделов
│   ├── staff_list.html          # Список сотрудников
│   └── partials/                # Переиспользуемые фрагменты
│       ├── wp_form.html         # Форма создания/редактирования
│       ├── wp_row.html          # Строка таблицы рабочего места
│       ├── wp_search.html       # Форма поиска
│       ├── task_status.html     # Статус Celery задачи
│       ├── spinner.html         # Индикатор загрузки
│       └── navmenu.html         # Меню навигации
│
├── static_src/                  # Исходные статические файлы
│   ├── css/styles.css           # Кастомные стили
│   └── js/base.js               # JavaScript для UI логики
│
├── Dockerfile                   # Docker образ приложения
├── docker-compose.yml           # Конфигурация всех сервисов
├── pyproject.toml               # Зависимости и конфиг UV/Ruff
├── manage.py                    # Django CLI
└── README.md                    # Этот файл
```

## Основные модели

### Workplaces

```
- name: CharField  # Название рабочего места
- description: TextField  # Описание
- type: CharField  # Тип: "pcplace" или "nopcplace"
- department: ForeignKey  # Связь на отдел
- ip: CharField  # IP адрес (только для pcplace)
- mac: CharField  # MAC адрес (только для pcplace)
- archived: BooleanField  # Флаг мягкого удаления
```

### Department

```
    - name: CharField  # Название отдела
    - description: TextField  # Описание
    - archived: BooleanField  # Флаг мягкого удаления
```

### Staff

```
- first_name: CharField  # Имя
- last_name: CharField  # Фамилия
- department: ForeignKey  # Связь на отдел
- email: EmailField  # Email
- phone: CharField  # Телефон
- archived: BooleanField  # Флаг мягкого удаления
```

## Командная строка

### Управление данными

```bash
# Заполнить БД тестовыми данными
uv run python manage.py populate_db

# Создать суперпользователя
uv run python manage.py createsuperuser

# Применить миграции
uv run python manage.py migrate

# Создать новые миграции
uv run python manage.py makemigrations
```

### Разработка

```bash
# Запустить сервер разработки
uv run python manage.py runserver

# Запустить Celery worker (требует Redis)
uv run celery -A macroemc_wmp worker --loglevel=info

# Запустить Celery beat (планировщик)
uv run celery -A macroemc_wmp beat --loglevel=info

# Форматирование кода
uv run black .

# Линтинг кода
uv run ruff check .
```

### Docker Compose

```bash
# Запустить все сервисы в фоне
docker-compose up -d

# Остановить сервисы
docker-compose down

# Просмотреть логи всех сервисов
docker-compose logs -f

# Просмотреть логи конкретного сервиса
docker-compose logs -f web

# Выполнить команду внутри контейнера
docker-compose exec web uv run python manage.py migrate

# Пересобрать образы
docker-compose up --build -d
```

## Архитектурные особенности

### HTMX интеграция

- Использование HTMX для асинхронных запросов без перезагрузки страницы
- Динамическое обновление таблицы при создании/удалении записей
- Валидация форм на клиенте и сервере

### Django Template Partials

- Переиспользуемые компоненты (wp_row.html, wp_form.html и др.)
- Инкрементальное обновление UI

### Celery для асинхронных операций

- Фоновая обработка создания рабочих мест
- Отслеживание статуса через task_status.html
- Автоматическое обновление UI при завершении

### Мягкое удаление

- Вместо физического удаления устанавливается флаг `archived=True`
- Активные записи фильтруются в querysets (`filter(archived=False)`)
- Данные сохраняются для истории и аудита

## Развертывание на производстве

1. **Используйте Gunicorn + Nginx**:

```bash
uv run pip install gunicorn
docker-compose build
docker-compose up -d
```

2. **Настройте переменные окружения**:
    - Установите `DEBUG=False`
    - Генерируйте `SECRET_KEY` с помощью `python manage.py shell`
    - Используйте надежные пароли для БД

3. **Используйте PostgreSQL** в production (уже в docker-compose)

4. **Включите HTTPS** через Nginx или облачный прокси

5. **Мониторьте Celery**:
    - Используйте Flower для мониторинга задач
    - Настройте логирование и alerting

## Решение проблем

### Ошибка подключения к БД

```bash
# Проверьте, что PostgreSQL запущен
docker-compose logs db

# Примените миграции вручную
docker-compose exec web uv run python manage.py migrate
```

### Celery задачи не выполняются

```bash
# Проверьте, что Redis запущен
docker-compose logs redis

# Проверьте логи worker'а
docker-compose logs celery

# Перезапустите worker
docker-compose restart celery
```

### HTMX запросы не работают

- Проверьте консоль браузера на ошибки
- Убедитесь, что Django HTMX middleware включен в settings.py
- Проверьте URL маршруты в urls.py

## Лицензия

Проект лицензирован под MIT License.

## Контакты

Автор: [fletch4503](https://github.com/fletch4503)

Репозиторий: [github.com/fletch4503/macroemc_wmp](https://github.com/fletch4503/macroemc_wmp)
