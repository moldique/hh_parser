"""
Модуль для работы с базой данных PostgreSQL
"""

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from typing import List, Dict, Any, Optional
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatabaseManager:
    """
    Класс для управления подключением к базе данных PostgreSQL
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
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.connection = None
    
    def connect(self) -> bool:
        """
        Подключение к базе данных
        
        Returns:
            bool: True если подключение успешно, False в противном случае
        """
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password
            )
            self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            logger.info(f"Успешное подключение к базе данных {self.database}")
            return True
        except psycopg2.Error as e:
            logger.error(f"Ошибка подключения к базе данных: {e}")
            return False
    
    def disconnect(self) -> None:
        """
        Отключение от базы данных
        """
        if self.connection:
            self.connection.close()
            logger.info("Отключение от базы данных")
    
    def create_database(self) -> bool:
        """
        Создание базы данных hh_parser
        
        Returns:
            bool: True если база данных создана успешно
        """
        try:
            # Подключаемся к базе postgres для создания новой БД
            temp_connection = psycopg2.connect(
                host=self.host,
                port=self.port,
                database="postgres",
                user=self.user,
                password=self.password
            )
            temp_connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            
            cursor = temp_connection.cursor()
            
            # Проверяем, существует ли база данных
            cursor.execute(
                "SELECT 1 FROM pg_database WHERE datname = %s",
                (self.database,)
            )
            
            if not cursor.fetchone():
                # Создаем базу данных
                cursor.execute(f'CREATE DATABASE "{self.database}"')
                logger.info(f"База данных {self.database} создана успешно")
            else:
                logger.info(f"База данных {self.database} уже существует")
            
            cursor.close()
            temp_connection.close()
            return True
            
        except psycopg2.Error as e:
            logger.error(f"Ошибка создания базы данных: {e}")
            return False
    
    def create_tables(self) -> bool:
        """
        Создание таблиц в базе данных
        
        Returns:
            bool: True если таблицы созданы успешно
        """
        if not self.connect():
            return False
        
        try:
            cursor = self.connection.cursor()
            
            # Создание таблицы компаний
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS companies (
                    id SERIAL PRIMARY KEY,
                    company_id INTEGER UNIQUE NOT NULL,
                    name VARCHAR(255) NOT NULL,
                    url VARCHAR(500),
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Создание таблицы вакансий
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS vacancies (
                    id SERIAL PRIMARY KEY,
                    vacancy_id INTEGER UNIQUE NOT NULL,
                    company_id INTEGER REFERENCES companies(company_id),
                    title VARCHAR(500) NOT NULL,
                    salary_from INTEGER,
                    salary_to INTEGER,
                    currency VARCHAR(10),
                    url VARCHAR(500),
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Создание индексов для оптимизации запросов
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_vacancies_company_id 
                ON vacancies(company_id)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_vacancies_salary_from 
                ON vacancies(salary_from)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_vacancies_title 
                ON vacancies(title)
            """)
            
            cursor.close()
            logger.info("Таблицы созданы успешно")
            return True
            
        except psycopg2.Error as e:
            logger.error(f"Ошибка создания таблиц: {e}")
            return False
        finally:
            self.disconnect()
    
    def execute_query(self, query: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
        """
        Выполнение SQL запроса
        
        Args:
            query: SQL запрос
            params: Параметры запроса
            
        Returns:
            List[Dict]: Результат запроса в виде списка словарей
        """
        if not self.connect():
            return []
        
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            
            # Получаем названия колонок
            columns = [desc[0] for desc in cursor.description]
            
            # Преобразуем результат в список словарей
            results = []
            for row in cursor.fetchall():
                results.append(dict(zip(columns, row)))
            
            cursor.close()
            return results
            
        except psycopg2.Error as e:
            logger.error(f"Ошибка выполнения запроса: {e}")
            return []
        finally:
            self.disconnect()
    
    def __enter__(self):
        """Контекстный менеджер - вход"""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Контекстный менеджер - выход"""
        self.disconnect()

