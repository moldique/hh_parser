"""
Класс DBManager для работы с данными в базе данных
"""

from database import DatabaseManager
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


class DBManager:
    """
    Класс для управления данными в базе данных PostgreSQL
    """
    
    def __init__(self, host: str = "localhost", port: int = 5432, 
                 database: str = "hh_parser", user: str = "postgres", 
                 password: str = "postgres"):
        """
        Инициализация менеджера базы данных
        
        Args:
            host: Хост базы данных
            port: Порт базы данных
            database: Имя базы данных
            user: Имя пользователя
            password: Пароль пользователя
        """
        self.db_manager = DatabaseManager(host, port, database, user, password)
    
    def get_companies_and_vacancies_count(self) -> List[Dict[str, Any]]:
        """
        Получает список всех компаний и количество вакансий у каждой компании
        
        Returns:
            List[Dict]: Список словарей с информацией о компаниях и количестве вакансий
        """
        query = """
            SELECT 
                c.name as company_name,
                COUNT(v.id) as vacancies_count
            FROM companies c
            LEFT JOIN vacancies v ON c.company_id = v.company_id
            GROUP BY c.company_id, c.name
            ORDER BY vacancies_count DESC
        """
        
        logger.info("Получение списка компаний и количества вакансий")
        return self.db_manager.execute_query(query)
    
    def get_all_vacancies(self) -> List[Dict[str, Any]]:
        """
        Получает список всех вакансий с указанием названия компании, 
        названия вакансии, зарплаты и ссылки на вакансию
        
        Returns:
            List[Dict]: Список словарей с информацией о вакансиях
        """
        query = """
            SELECT 
                c.name as company_name,
                v.title as vacancy_title,
                CASE 
                    WHEN v.salary_from IS NOT NULL AND v.salary_to IS NOT NULL THEN
                        CONCAT(v.salary_from, ' - ', v.salary_to, ' ', v.currency)
                    WHEN v.salary_from IS NOT NULL THEN
                        CONCAT('от ', v.salary_from, ' ', v.currency)
                    WHEN v.salary_to IS NOT NULL THEN
                        CONCAT('до ', v.salary_to, ' ', v.currency)
                    ELSE 'Зарплата не указана'
                END as salary,
                v.url as vacancy_url
            FROM vacancies v
            JOIN companies c ON v.company_id = c.company_id
            ORDER BY c.name, v.title
        """
        
        logger.info("Получение списка всех вакансий")
        return self.db_manager.execute_query(query)
    
    def get_avg_salary(self) -> float:
        """
        Получает среднюю зарплату по всем вакансиям
        
        Returns:
            float: Средняя зарплата
        """
        query = """
            SELECT AVG(
                CASE 
                    WHEN salary_from IS NOT NULL AND salary_to IS NOT NULL THEN
                        (salary_from + salary_to) / 2
                    WHEN salary_from IS NOT NULL THEN
                        salary_from
                    WHEN salary_to IS NOT NULL THEN
                        salary_to
                    ELSE NULL
                END
            ) as avg_salary
            FROM vacancies
            WHERE salary_from IS NOT NULL OR salary_to IS NOT NULL
        """
        
        logger.info("Получение средней зарплаты")
        result = self.db_manager.execute_query(query)
        
        if result and result[0]['avg_salary']:
            return round(float(result[0]['avg_salary']), 2)
        return 0.0
    
    def get_vacancies_with_higher_salary(self) -> List[Dict[str, Any]]:
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям
        
        Returns:
            List[Dict]: Список вакансий с зарплатой выше средней
        """
        query = """
            WITH avg_salary AS (
                SELECT AVG(
                    CASE 
                        WHEN salary_from IS NOT NULL AND salary_to IS NOT NULL THEN
                            (salary_from + salary_to) / 2
                        WHEN salary_from IS NOT NULL THEN
                            salary_from
                        WHEN salary_to IS NOT NULL THEN
                            salary_to
                        ELSE NULL
                    END
                ) as avg_sal
                FROM vacancies
                WHERE salary_from IS NOT NULL OR salary_to IS NOT NULL
            )
            SELECT 
                c.name as company_name,
                v.title as vacancy_title,
                CASE 
                    WHEN v.salary_from IS NOT NULL AND v.salary_to IS NOT NULL THEN
                        CONCAT(v.salary_from, ' - ', v.salary_to, ' ', v.currency)
                    WHEN v.salary_from IS NOT NULL THEN
                        CONCAT('от ', v.salary_from, ' ', v.currency)
                    WHEN v.salary_to IS NOT NULL THEN
                        CONCAT('до ', v.salary_to, ' ', v.currency)
                    ELSE 'Зарплата не указана'
                END as salary,
                v.url as vacancy_url
            FROM vacancies v
            JOIN companies c ON v.company_id = c.company_id
            CROSS JOIN avg_salary
            WHERE (
                CASE 
                    WHEN v.salary_from IS NOT NULL AND v.salary_to IS NOT NULL THEN
                        (v.salary_from + v.salary_to) / 2
                    WHEN v.salary_from IS NOT NULL THEN
                        v.salary_from
                    WHEN v.salary_to IS NOT NULL THEN
                        v.salary_to
                    ELSE NULL
                END
            ) > avg_salary.avg_sal
            ORDER BY 
                CASE 
                    WHEN v.salary_from IS NOT NULL AND v.salary_to IS NOT NULL THEN
                        (v.salary_from + v.salary_to) / 2
                    WHEN v.salary_from IS NOT NULL THEN
                        v.salary_from
                    WHEN v.salary_to IS NOT NULL THEN
                        v.salary_to
                    ELSE 0
                END DESC
        """
        
        logger.info("Получение вакансий с зарплатой выше средней")
        return self.db_manager.execute_query(query)
    
    def get_vacancies_with_keyword(self, keyword: str) -> List[Dict[str, Any]]:
        """
        Получает список всех вакансий, в названии которых содержатся переданные слова
        
        Args:
            keyword: Ключевое слово для поиска (например, "python")
            
        Returns:
            List[Dict]: Список вакансий, содержащих ключевое слово в названии
        """
        query = """
            SELECT 
                c.name as company_name,
                v.title as vacancy_title,
                CASE 
                    WHEN v.salary_from IS NOT NULL AND v.salary_to IS NOT NULL THEN
                        CONCAT(v.salary_from, ' - ', v.salary_to, ' ', v.currency)
                    WHEN v.salary_from IS NOT NULL THEN
                        CONCAT('от ', v.salary_from, ' ', v.currency)
                    WHEN v.salary_to IS NOT NULL THEN
                        CONCAT('до ', v.salary_to, ' ', v.currency)
                    ELSE 'Зарплата не указана'
                END as salary,
                v.url as vacancy_url
            FROM vacancies v
            JOIN companies c ON v.company_id = c.company_id
            WHERE LOWER(v.title) LIKE LOWER(%s)
            ORDER BY c.name, v.title
        """
        
        search_pattern = f"%{keyword}%"
        logger.info(f"Поиск вакансий по ключевому слову: {keyword}")
        return self.db_manager.execute_query(query, (search_pattern,))
    
    def insert_company(self, company_id: int, name: str, url: str = None, 
                      description: str = None) -> bool:
        """
        Вставка компании в базу данных
        
        Args:
            company_id: ID компании на hh.ru
            name: Название компании
            url: URL компании
            description: Описание компании
            
        Returns:
            bool: True если вставка успешна
        """
        query = """
            INSERT INTO companies (company_id, name, url, description)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (company_id) DO UPDATE SET
                name = EXCLUDED.name,
                url = EXCLUDED.url,
                description = EXCLUDED.description
        """
        
        try:
            if self.db_manager.connect():
                cursor = self.db_manager.connection.cursor()
                cursor.execute(query, (company_id, name, url, description))
                cursor.close()
                logger.info(f"Компания {name} добавлена в базу данных")
                return True
        except Exception as e:
            logger.error(f"Ошибка при добавлении компании: {e}")
        finally:
            self.db_manager.disconnect()
        
        return False
    
    def insert_vacancy(self, vacancy_id: int, company_id: int, title: str,
                      salary_from: int = None, salary_to: int = None,
                      currency: str = None, url: str = None,
                      description: str = None) -> bool:
        """
        Вставка вакансии в базу данных
        
        Args:
            vacancy_id: ID вакансии на hh.ru
            company_id: ID компании
            title: Название вакансии
            salary_from: Зарплата от
            salary_to: Зарплата до
            currency: Валюта
            url: URL вакансии
            description: Описание вакансии
            
        Returns:
            bool: True если вставка успешна
        """
        query = """
            INSERT INTO vacancies (vacancy_id, company_id, title, salary_from, 
                                 salary_to, currency, url, description)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (vacancy_id) DO UPDATE SET
                company_id = EXCLUDED.company_id,
                title = EXCLUDED.title,
                salary_from = EXCLUDED.salary_from,
                salary_to = EXCLUDED.salary_to,
                currency = EXCLUDED.currency,
                url = EXCLUDED.url,
                description = EXCLUDED.description
        """
        
        try:
            if self.db_manager.connect():
                cursor = self.db_manager.connection.cursor()
                cursor.execute(query, (vacancy_id, company_id, title, salary_from,
                                     salary_to, currency, url, description))
                cursor.close()
                logger.info(f"Вакансия {title} добавлена в базу данных")
                return True
        except Exception as e:
            logger.error(f"Ошибка при добавлении вакансии: {e}")
        finally:
            self.db_manager.disconnect()
        
        return False
