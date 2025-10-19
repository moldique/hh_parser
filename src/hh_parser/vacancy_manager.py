"""
Модуль для управления вакансиями
"""

from typing import List, Dict, Any, Optional
from api_client import HeadHunterAPI
from db_manager import DBManager
import logging

logger = logging.getLogger(__name__)


class VacancyManager:
    """
    Класс для управления вакансиями и их обработки
    """
    
    def __init__(self, db_manager: DBManager):
        """
        Инициализация менеджера вакансий
        
        Args:
            db_manager: Экземпляр DBManager для работы с базой данных
        """
        self.api = HeadHunterAPI()
        self.db_manager = db_manager
    
    def collect_company_data(self, company_ids: List[int], 
                           max_vacancies_per_company: int = 100) -> Dict[str, Any]:
        """
        Сбор данных о компаниях и их вакансиях
        
        Args:
            company_ids: Список ID компаний для сбора данных
            max_vacancies_per_company: Максимальное количество вакансий на компанию
            
        Returns:
            Dict: Статистика сбора данных
        """
        stats = {
            'companies_processed': 0,
            'companies_failed': 0,
            'vacancies_collected': 0,
            'vacancies_failed': 0
        }
        
        logger.info(f"Начинаем сбор данных для {len(company_ids)} компаний")
        
        for company_id in company_ids:
            try:
                # Получаем информацию о компании
                company_info = self.api.get_company_info(company_id)
                if not company_info:
                    stats['companies_failed'] += 1
                    continue
                
                # Сохраняем компанию в базу данных
                success = self.db_manager.insert_company(
                    company_id=company_info['id'],
                    name=company_info['name'],
                    url=company_info.get('url'),
                    description=company_info.get('description')
                )
                
                if not success:
                    stats['companies_failed'] += 1
                    continue
                
                stats['companies_processed'] += 1
                
                # Получаем вакансии компании
                vacancies = self.api.get_company_vacancies(
                    company_id, 
                    max_vacancies_per_company
                )
                
                # Сохраняем вакансии в базу данных
                for vacancy in vacancies:
                    success = self.db_manager.insert_vacancy(
                        vacancy_id=vacancy['id'],
                        company_id=vacancy['company_id'],
                        title=vacancy['title'],
                        salary_from=vacancy.get('salary_from'),
                        salary_to=vacancy.get('salary_to'),
                        currency=vacancy.get('currency'),
                        url=vacancy.get('url'),
                        description=vacancy.get('description')
                    )
                    
                    if success:
                        stats['vacancies_collected'] += 1
                    else:
                        stats['vacancies_failed'] += 1
                
                logger.info(f"Обработана компания {company_info['name']}: "
                           f"{len(vacancies)} вакансий")
                
            except Exception as e:
                logger.error(f"Ошибка при обработке компании {company_id}: {e}")
                stats['companies_failed'] += 1
        
        logger.info(f"Сбор данных завершен. Статистика: {stats}")
        return stats
    
    def search_and_collect_vacancies(self, keywords: List[str], 
                                   max_vacancies_per_keyword: int = 10) -> Dict[str, Any]:
        """
        Поиск и сбор вакансий по ключевым словам
        
        Args:
            keywords: Список ключевых слов для поиска
            max_vacancies_per_keyword: Максимальное количество вакансий на ключевое слово
            
        Returns:
            Dict: Статистика сбора данных
        """
        stats = {
            'keywords_processed': 0,
            'vacancies_collected': 0,
            'vacancies_failed': 0
        }
        
        logger.info(f"Начинаем поиск вакансий по ключевым словам: {keywords}")
        
        for keyword in keywords:
            try:
                # Получаем вакансии по ключевому слову
                vacancies = self.api.get_vacancies_by_keyword(
                    keyword, 
                    per_page=max_vacancies_per_keyword
                )
                
                # Обрабатываем каждую вакансию
                for vacancy in vacancies:
                    # Сначала сохраняем компанию, если её нет
                    if vacancy.get('company_id'):
                        company_info = self.api.get_company_info(vacancy['company_id'])
                        if company_info:
                            self.db_manager.insert_company(
                                company_id=company_info['id'],
                                name=company_info['name'],
                                url=company_info.get('url'),
                                description=company_info.get('description')
                            )
                    
                    # Сохраняем вакансию
                    success = self.db_manager.insert_vacancy(
                        vacancy_id=vacancy['id'],
                        company_id=vacancy.get('company_id'),
                        title=vacancy['title'],
                        salary_from=vacancy.get('salary_from'),
                        salary_to=vacancy.get('salary_to'),
                        currency=vacancy.get('currency'),
                        url=vacancy.get('url'),
                        description=vacancy.get('description')
                    )
                    
                    if success:
                        stats['vacancies_collected'] += 1
                    else:
                        stats['vacancies_failed'] += 1
                
                stats['keywords_processed'] += 1
                logger.info(f"Обработано ключевое слово '{keyword}': "
                           f"{len(vacancies)} вакансий")
                
            except Exception as e:
                logger.error(f"Ошибка при поиске по ключевому слову '{keyword}': {e}")
        
        logger.info(f"Поиск по ключевым словам завершен. Статистика: {stats}")
        return stats
    
    def get_vacancy_statistics(self) -> Dict[str, Any]:
        """
        Получение статистики по вакансиям
        
        Returns:
            Dict: Статистика вакансий
        """
        try:
            # Получаем общее количество вакансий
            total_vacancies = len(self.db_manager.get_all_vacancies())
            
            # Получаем среднюю зарплату
            avg_salary = self.db_manager.get_avg_salary()
            
            # Получаем количество компаний
            companies = self.db_manager.get_companies_and_vacancies_count()
            total_companies = len(companies)
            
            # Получаем вакансии с высокой зарплатой
            high_salary_vacancies = self.db_manager.get_vacancies_with_higher_salary()
            
            return {
                'total_vacancies': total_vacancies,
                'total_companies': total_companies,
                'average_salary': avg_salary,
                'high_salary_vacancies_count': len(high_salary_vacancies)
            }
            
        except Exception as e:
            logger.error(f"Ошибка при получении статистики: {e}")
            return {}
    
    def export_vacancies_to_file(self, filename: str, 
                               format_type: str = 'csv') -> bool:
        """
        Экспорт вакансий в файл
        
        Args:
            filename: Имя файла для экспорта
            format_type: Тип формата ('csv', 'json')
            
        Returns:
            bool: True если экспорт успешен
        """
        try:
            vacancies = self.db_manager.get_all_vacancies()
            
            if format_type.lower() == 'csv':
                import csv
                with open(filename, 'w', newline='', encoding='utf-8') as file:
                    if vacancies:
                        writer = csv.DictWriter(file, fieldnames=vacancies[0].keys())
                        writer.writeheader()
                        writer.writerows(vacancies)
            
            elif format_type.lower() == 'json':
                import json
                with open(filename, 'w', encoding='utf-8') as file:
                    json.dump(vacancies, file, ensure_ascii=False, indent=2)
            
            logger.info(f"Экспорт вакансий в файл {filename} завершен")
            return True
            
        except Exception as e:
            logger.error(f"Ошибка при экспорте в файл: {e}")
            return False
