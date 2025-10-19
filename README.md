# hh_parser

Парсер вакансий с HeadHunter для анализа рынка труда.

**GitHub:** [https://github.com/moldique/hh_parser](https://github.com/moldique/hh_parser)

## Установка и настройка

### Требования
- Python 3.8+
- Poetry

### Установка проекта

1. Клонируйте репозиторий:
```bash
git clone https://github.com/moldique/hh_parser.git
cd hh_parser
```

2. Установите Poetry, если еще не установлен:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

3. Установите зависимости проекта:
```bash
poetry install
```

4. Активируйте виртуальное окружение:
```bash
poetry shell
```

### Запуск проекта

```bash
# Способ 1: Основная версия (с API HeadHunter)
poetry run python -m hh_parser.main

# Способ 2: Через активированное окружение
poetry shell
python -m hh_parser.main
```

**Приложение автоматически создаст базу данных и соберет до 50 вакансий для демонстрации!**

### Разработка

```bash
# Установка зависимостей для разработки
poetry install --with dev

# Запуск тестов
poetry run pytest

# Форматирование кода
poetry run black src/ tests/

# Проверка стиля кода
poetry run flake8 src/ tests/

# Проверка типов
poetry run mypy src/
```

## Структура проекта

```
hh_parser/
├── src/
│   └── hh_parser/
│       ├── __init__.py
│       ├── main.py                 # Точка входа в программу
│       ├── database.py             # Модуль для работы с БД
│       ├── db_manager.py           # Класс DBManager
│       ├── api_client.py           # Модуль для работы с API hh.ru
│       ├── vacancy_manager.py      # Модуль для управления вакансиями
│       ├── user_interface.py       # Интерфейс взаимодействия с пользователем
│       ├── setup_database.py       # Скрипт создания БД и таблиц
│       └── config.py               # Конфигурация проекта
├── pyproject.toml
├── .gitignore
└── README.md
```

## Функциональность

### Основные модули:
- **`main.py`** - точка входа, запускает парсинг и интерактивный интерфейс
- **`database.py`** - базовые функции для работы с PostgreSQL
- **`db_manager.py`** - класс DBManager с методами для анализа данных
- **`api_client.py`** - работа с API HeadHunter
- **`vacancy_manager.py`** - управление вакансиями и сбор данных
- **`user_interface.py`** - интерактивный интерфейс для пользователя

### Возможности:
- ✅ Автоматическое создание БД и таблиц
- ✅ Парсинг данных с hh.ru через API (до 50 вакансий)
- ✅ Сохранение данных в PostgreSQL
- ✅ Анализ вакансий и компаний
- ✅ Поиск по ключевым словам
- ✅ Расчет средней зарплаты
- ✅ Интерактивный интерфейс
- ✅ Логирование всех операций
- ✅ Ограниченный сбор данных для быстрой демонстрации

## Настройка базы данных

Приложение автоматически создаст базу данных `hh_parser` и необходимые таблицы при первом запуске.

### Ручная настройка (если нужно):
```bash
poetry run python -m hh_parser.setup_database
```

## Требования к системе

- Python 3.8+
- PostgreSQL (локально или в Docker)
- Poetry для управления зависимостями