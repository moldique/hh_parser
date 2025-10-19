"""
Основной модуль парсера HeadHunter
"""

import logging
from db_manager import DBManager
from vacancy_manager import VacancyManager
from user_interface import UserInterface
from setup_database import setup_database

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """
    Главная функция парсера HeadHunter
    """
    print("=== Парсер вакансий HeadHunter ===")
    print("Инициализация системы...")

    try:
        # Создаем базу данных и таблицы
        print("Создание базы данных и таблиц...")
        if not setup_database():
            print("[ERROR] Ошибка при создании базы данных")
            return

        # Инициализируем менеджеры
        db_manager = DBManager()
        vacancy_manager = VacancyManager(db_manager)

        # Поиск вакансий по ключевым словам (работающий способ)
        keywords = [
            "python",
            "java",
            "javascript",
            "developer",
            "программист",
            "аналитик",
            "менеджер",
            "дизайнер"
        ]

        print(f"Поиск вакансий по ключевым словам: {keywords}")

        # Собираем вакансии по ключевым словам (ограничиваем до 50 вакансий)
        stats = vacancy_manager.search_and_collect_vacancies(
            keywords, max_vacancies_per_keyword=5
        )

        print("\n=== Статистика сбора данных ===")
        if 'companies_processed' in stats:
            print(f"Обработано компаний: {stats['companies_processed']}")
            print(f"Ошибок компаний: {stats['companies_failed']}")
        else:
            print(f"Обработано ключевых слов: {stats.get('keywords_processed', 0)}")
        print(f"Собрано вакансий: {stats['vacancies_collected']}")
        print(f"Ошибок вакансий: {stats['vacancies_failed']}")

        # Получаем статистику по собранным данным
        print("\n=== Статистика базы данных ===")
        db_stats = vacancy_manager.get_vacancy_statistics()
        print(f"Всего компаний в БД: {db_stats.get('total_companies', 0)}")
        print(f"Всего вакансий в БД: {db_stats.get('total_vacancies', 0)}")
        print(f"Средняя зарплата: {db_stats.get('average_salary', 0)} руб.")
        high_salary_count = db_stats.get('high_salary_vacancies_count', 0)
        print(f"Вакансий с зарплатой выше средней: {high_salary_count}")

        # Демонстрация работы методов DBManager
        print("\n=== Демонстрация работы с данными ===")

        # Получаем компании и количество вакансий
        companies = db_manager.get_companies_and_vacancies_count()
        print("\nТоп-5 компаний по количеству вакансий:")
        for i, company in enumerate(companies[:5], 1):
            print(f"{i}. {company['company_name']}: {company['vacancies_count']} вакансий")

        # Получаем среднюю зарплату
        avg_salary = db_manager.get_avg_salary()
        print(f"\nСредняя зарплата по всем вакансиям: {avg_salary} руб.")

        # Получаем вакансии с высокой зарплатой
        high_salary_vacancies = db_manager.get_vacancies_with_higher_salary()
        print("\nВакансии с зарплатой выше средней (первые 3):")
        for i, vacancy in enumerate(high_salary_vacancies[:3], 1):
            print(f"{i}. {vacancy['company_name']} - {vacancy['vacancy_title']}")
            print(f"   Зарплата: {vacancy['salary']}")

        # Поиск вакансий по ключевому слову
        python_vacancies = db_manager.get_vacancies_with_keyword("python")
        print(f"\nНайдено {len(python_vacancies)} вакансий со словом 'python'")

        print("\n[SUCCESS] Парсер HeadHunter завершил работу успешно!")

        # Запуск интерактивного интерфейса
        print("\n" + "="*50)
        user_input = input("Хотите запустить интерактивный интерфейс? (y/n): ").strip().lower()

        if user_input in ['y', 'yes', 'да', 'д']:
            user_interface = UserInterface(db_manager)
            user_interface.interactive_menu()

    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")
        print(f"[ERROR] Ошибка выполнения: {e}")


if __name__ == "__main__":
    main()
