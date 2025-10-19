"""
Конфигурация проекта
"""

# Настройки базы данных
DATABASE_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'hh_parser',
    'user': 'postgres',
    'password': 'postgres'
}

# Настройки API HeadHunter
API_CONFIG = {
    'base_url': 'https://api.hh.ru',
    'user_agent': 'hh_parser/1.0 (contact@example.com)',
    'request_delay': 0.25,  # Задержка между запросами в секундах
    'max_vacancies_per_company': 100,
    'max_vacancies_per_keyword': 50
}

# Список популярных IT-компаний для парсинга
POPULAR_COMPANIES = [
    {'id': 1740, 'name': 'Яндекс'},
    {'id': 3529, 'name': 'Сбер'},
    {'id': 78638, 'name': 'Тинькофф'},
    {'id': 15478, 'name': 'VK'},
    {'id': 1122462, 'name': 'Ozon'},
    {'id': 2180, 'name': 'Mail.ru Group'},
    {'id': 2381, 'name': 'Авито'},
    {'id': 3776, 'name': 'МегаФон'},
    {'id': 25324, 'name': 'Ростелеком'},
    {'id': 87021, 'name': '2ГИС'},
    {'id': 84585, 'name': 'Лаборатория Касперского'},
    {'id': 1057, 'name': 'МТС'},
    {'id': 4181, 'name': 'Рамблер'},
    {'id': 1373, 'name': 'Роснефть'},
    {'id': 1272486, 'name': 'Wildberries'}
]

# Ключевые слова для поиска вакансий
SEARCH_KEYWORDS = [
    'python',
    'java',
    'javascript',
    'developer',
    'программист',
    'аналитик',
    'менеджер',
    'дизайнер'
]

# Настройки логирования
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'filename': 'hh_parser.log'
}

# Настройки экспорта данных
EXPORT_CONFIG = {
    'default_format': 'csv',
    'output_directory': 'output',
    'filename_template': 'vacancies_{timestamp}'
}

