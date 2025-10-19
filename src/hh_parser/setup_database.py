"""
Скрипт для создания базы данных и таблиц
"""

import sys
from database import DatabaseManager
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def setup_database():
    """
    Создание базы данных и таблиц
    """
    logger.info("Начинаем настройку базы данных...")

    # Создаем экземпляр менеджера базы данных
    db_manager = DatabaseManager()

    try:
        # Создаем базу данных
        logger.info("Создание базы данных...")
        if not db_manager.create_database():
            logger.error("Не удалось создать базу данных")
            return False

        # Создаем таблицы
        logger.info("Создание таблиц...")
        if not db_manager.create_tables():
            logger.error("Не удалось создать таблицы")
            return False

        logger.info("База данных и таблицы созданы успешно!")
        return True

    except Exception as e:
        logger.error(f"Ошибка при настройке базы данных: {e}")
        return False


def main():
    """
    Главная функция для настройки базы данных
    """
    print("=== Настройка базы данных для hh_parser ===")
    print("Создание базы данных и таблиц...")

    if setup_database():
        print("[SUCCESS] База данных настроена успешно!")
        print("Созданы таблицы:")
        print("  - companies (компании)")
        print("  - vacancies (вакансии)")
        print("  - Индексы для оптимизации запросов")
    else:
        print("[ERROR] Ошибка при настройке базы данных")
        sys.exit(1)


if __name__ == "__main__":
    main()
