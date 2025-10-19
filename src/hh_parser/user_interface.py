"""
Интерфейс взаимодействия с пользователем
"""

from db_manager import DBManager
import logging

logger = logging.getLogger(__name__)


class UserInterface:
    """
    Класс для взаимодействия с пользователем
    """

    def __init__(self, db_manager: DBManager):
        """
        Инициализация интерфейса пользователя

        Args:
            db_manager: Экземпляр DBManager для работы с базой данных
        """
        self.db_manager = db_manager

    def show_companies_and_vacancies_count(self) -> None:
        """
        Показать список всех компаний и количество вакансий у каждой компании
        """
        print("\n=== Компании и количество вакансий ===")

        try:
            companies = self.db_manager.get_companies_and_vacancies_count()

            if not companies:
                print("Компании не найдены в базе данных")
                return

            print(f"Найдено {len(companies)} компаний:")
            print("-" * 50)

            for i, company in enumerate(companies, 1):
                print(f"{i}. {company['company_name']}: {company['vacancies_count']} вакансий")

        except Exception as e:
            logger.error(f"Ошибка при получении списка компаний: {e}")
            print("Ошибка при получении данных о компаниях")

    def show_all_vacancies(self, limit: int = 10) -> None:
        """
        Показать список всех вакансий

        Args:
            limit: Максимальное количество вакансий для отображения
        """
        print(f"\n=== Все вакансии (показано {limit} из общего количества) ===")

        try:
            vacancies = self.db_manager.get_all_vacancies()

            if not vacancies:
                print("Вакансии не найдены в базе данных")
                return

            print(f"Всего вакансий в базе: {len(vacancies)}")
            print("-" * 80)

            for i, vacancy in enumerate(vacancies[:limit], 1):
                print(f"{i}. Компания: {vacancy['company_name']}")
                print(f"   Должность: {vacancy['vacancy_title']}")
                print(f"   Зарплата: {vacancy['salary']}")
                print(f"   Ссылка: {vacancy['vacancy_url']}")
                print()

            if len(vacancies) > limit:
                print(f"... и еще {len(vacancies) - limit} вакансий")

        except Exception as e:
            logger.error(f"Ошибка при получении списка вакансий: {e}")
            print("Ошибка при получении данных о вакансиях")

    def show_average_salary(self) -> None:
        """
        Показать среднюю зарплату по всем вакансиям
        """
        print("\n=== Средняя зарплата ===")

        try:
            avg_salary = self.db_manager.get_avg_salary()

            if avg_salary > 0:
                print(f"Средняя зарплата по всем вакансиям: {avg_salary:,.0f} руб.")
            else:
                print("Не удалось рассчитать среднюю зарплату")

        except Exception as e:
            logger.error(f"Ошибка при расчете средней зарплаты: {e}")
            print("Ошибка при получении данных о зарплате")

    def show_vacancies_with_higher_salary(self, limit: int = 5) -> None:
        """
        Показать вакансии с зарплатой выше средней

        Args:
            limit: Максимальное количество вакансий для отображения
        """
        print(f"\n=== Вакансии с зарплатой выше средней (показано {limit}) ===")

        try:
            high_salary_vacancies = self.db_manager.get_vacancies_with_higher_salary()

            if not high_salary_vacancies:
                print("Вакансии с высокой зарплатой не найдены")
                return

            print(f"Найдено {len(high_salary_vacancies)} вакансий с зарплатой выше средней:")
            print("-" * 80)

            for i, vacancy in enumerate(high_salary_vacancies[:limit], 1):
                print(f"{i}. Компания: {vacancy['company_name']}")
                print(f"   Должность: {vacancy['vacancy_title']}")
                print(f"   Зарплата: {vacancy['salary']}")
                print(f"   Ссылка: {vacancy['vacancy_url']}")
                print()

            if len(high_salary_vacancies) > limit:
                print(f"... и еще {len(high_salary_vacancies) - limit} вакансий")

        except Exception as e:
            logger.error(f"Ошибка при получении вакансий с высокой зарплатой: {e}")
            print("Ошибка при получении данных о вакансиях с высокой зарплатой")

    def search_vacancies_by_keyword(self, keyword: str, limit: int = 5) -> None:
        """
        Поиск вакансий по ключевому слову

        Args:
            keyword: Ключевое слово для поиска
            limit: Максимальное количество вакансий для отображения
        """
        print(f"\n=== Поиск вакансий по ключевому слову '{keyword}' ===")

        try:
            vacancies = self.db_manager.get_vacancies_with_keyword(keyword)

            if not vacancies:
                print(f"Вакансии со словом '{keyword}' не найдены")
                return

            print(f"Найдено {len(vacancies)} вакансий со словом '{keyword}':")
            print("-" * 80)

            for i, vacancy in enumerate(vacancies[:limit], 1):
                print(f"{i}. Компания: {vacancy['company_name']}")
                print(f"   Должность: {vacancy['vacancy_title']}")
                print(f"   Зарплата: {vacancy['salary']}")
                print(f"   Ссылка: {vacancy['vacancy_url']}")
                print()

            if len(vacancies) > limit:
                print(f"... и еще {len(vacancies) - limit} вакансий")

        except Exception as e:
            logger.error(f"Ошибка при поиске вакансий по ключевому слову: {e}")
            print("Ошибка при поиске вакансий")

    def show_database_statistics(self) -> None:
        """
        Показать общую статистику базы данных
        """
        print("\n=== Статистика базы данных ===")

        try:
            # Получаем общую статистику
            companies = self.db_manager.get_companies_and_vacancies_count()
            all_vacancies = self.db_manager.get_all_vacancies()
            avg_salary = self.db_manager.get_avg_salary()
            high_salary_vacancies = self.db_manager.get_vacancies_with_higher_salary()

            print(f"Всего компаний: {len(companies)}")
            print(f"Всего вакансий: {len(all_vacancies)}")
            print(f"Средняя зарплата: {avg_salary:,.0f} руб.")
            print(f"Вакансий с зарплатой выше средней: {len(high_salary_vacancies)}")

            # Топ-3 компании по количеству вакансий
            if companies:
                print("\nТоп-3 компании по количеству вакансий:")
                for i, company in enumerate(companies[:3], 1):
                    print(f"{i}. {company['company_name']}: {company['vacancies_count']} вакансий")

        except Exception as e:
            logger.error(f"Ошибка при получении статистики: {e}")
            print("Ошибка при получении статистики базы данных")

    def interactive_menu(self) -> None:
        """
        Интерактивное меню для взаимодействия с пользователем
        """
        while True:
            print("\n" + "="*50)
            print("ПАРСЕР ВАКАНСИЙ HEADHUNTER")
            print("="*50)
            print("1. Показать компании и количество вакансий")
            print("2. Показать все вакансии")
            print("3. Показать среднюю зарплату")
            print("4. Показать вакансии с зарплатой выше средней")
            print("5. Поиск вакансий по ключевому слову")
            print("6. Показать статистику базы данных")
            print("0. Выход")
            print("-"*50)

            try:
                choice = input("Выберите опцию (0-6): ").strip()

                if choice == "0":
                    print("До свидания!")
                    break
                elif choice == "1":
                    self.show_companies_and_vacancies_count()
                elif choice == "2":
                    limit = input("Сколько вакансий показать? (по умолчанию 10): ").strip()
                    limit = int(limit) if limit.isdigit() else 10
                    self.show_all_vacancies(limit)
                elif choice == "3":
                    self.show_average_salary()
                elif choice == "4":
                    limit = input("Сколько вакансий показать? (по умолчанию 5): ").strip()
                    limit = int(limit) if limit.isdigit() else 5
                    self.show_vacancies_with_higher_salary(limit)
                elif choice == "5":
                    keyword = input("Введите ключевое слово для поиска: ").strip()
                    if keyword:
                        limit = input("Сколько вакансий показать? (по умолчанию 5): ").strip()
                        limit = int(limit) if limit.isdigit() else 5
                        self.search_vacancies_by_keyword(keyword, limit)
                    else:
                        print("Ключевое слово не может быть пустым")
                elif choice == "6":
                    self.show_database_statistics()
                else:
                    print("Неверный выбор. Попробуйте снова.")

                input("\nНажмите Enter для продолжения...")

            except KeyboardInterrupt:
                print("\n\nПрограмма прервана пользователем")
                break
            except Exception as e:
                logger.error(f"Ошибка в интерактивном меню: {e}")
                print(f"Произошла ошибка: {e}")
                input("Нажмите Enter для продолжения...")
