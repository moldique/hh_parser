"""
Модуль для работы с API HeadHunter
"""

import requests
import time
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class HeadHunterAPI:
    """
    Класс для работы с API HeadHunter
    """
    
    def __init__(self):
        """
        Инициализация API клиента
        """
        self.base_url = "https://api.hh.ru"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json',
            'Accept-Language': 'ru-RU,ru;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
    
    def get_company_info(self, company_id: int) -> Optional[Dict[str, Any]]:
        """
        Получение информации о компании по ID
        
        Args:
            company_id: ID компании на hh.ru
            
        Returns:
            Dict: Информация о компании или None при ошибке
        """
        url = f"{self.base_url}/employers/{company_id}"
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"Получена информация о компании {company_id}")
            
            return {
                'id': data.get('id'),
                'name': data.get('name'),
                'url': data.get('site_url'),
                'description': data.get('description')
            }
            
        except requests.RequestException as e:
            logger.error(f"Ошибка при получении информации о компании {company_id}: {e}")
            return None
    
    def get_company_vacancies(self, company_id: int, per_page: int = 100) -> List[Dict[str, Any]]:
        """
        Получение вакансий компании
        
        Args:
            company_id: ID компании
            per_page: Количество вакансий на страницу (максимум 100)
            
        Returns:
            List[Dict]: Список вакансий компании
        """
        url = f"{self.base_url}/vacancies"
        params = {
            'employer_id': company_id,
            'per_page': min(per_page, 100),
            'page': 0
        }
        
        all_vacancies = []
        
        try:
            while True:
                response = self.session.get(url, params=params)
                response.raise_for_status()
                
                data = response.json()
                vacancies = data.get('items', [])
                
                if not vacancies:
                    break
                
                # Обрабатываем каждую вакансию
                for vacancy in vacancies:
                    processed_vacancy = self._process_vacancy(vacancy)
                    if processed_vacancy:
                        all_vacancies.append(processed_vacancy)
                
                # Проверяем, есть ли еще страницы
                if params['page'] >= data.get('pages', 1) - 1:
                    break
                
                params['page'] += 1
                
                # Пауза между запросами для соблюдения лимитов API
                time.sleep(0.25)
            
            logger.info(f"Получено {len(all_vacancies)} вакансий для компании {company_id}")
            return all_vacancies
            
        except requests.RequestException as e:
            logger.error(f"Ошибка при получении вакансий компании {company_id}: {e}")
            return []
    
    def _process_vacancy(self, vacancy: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Обработка данных вакансии
        
        Args:
            vacancy: Сырые данные вакансии из API
            
        Returns:
            Dict: Обработанные данные вакансии
        """
        try:
            salary = vacancy.get('salary')
            salary_from = None
            salary_to = None
            currency = None
            
            if salary:
                salary_from = salary.get('from')
                salary_to = salary.get('to')
                currency = salary.get('currency')
            
            return {
                'id': vacancy.get('id'),
                'title': vacancy.get('name'),
                'company_id': vacancy.get('employer', {}).get('id'),
                'salary_from': salary_from,
                'salary_to': salary_to,
                'currency': currency,
                'url': vacancy.get('alternate_url'),
                'description': vacancy.get('description', '')[:1000]  # Ограничиваем описание
            }
            
        except Exception as e:
            logger.error(f"Ошибка при обработке вакансии: {e}")
            return None
    
    def search_companies(self, query: str, per_page: int = 20) -> List[Dict[str, Any]]:
        """
        Поиск компаний по запросу
        
        Args:
            query: Поисковый запрос
            per_page: Количество результатов на страницу
            
        Returns:
            List[Dict]: Список найденных компаний
        """
        url = f"{self.base_url}/employers"
        params = {
            'text': query,
            'per_page': per_page
        }
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            companies = data.get('items', [])
            
            logger.info(f"Найдено {len(companies)} компаний по запросу '{query}'")
            
            return [
                {
                    'id': company.get('id'),
                    'name': company.get('name'),
                    'url': company.get('site_url'),
                    'description': company.get('description', '')[:500]
                }
                for company in companies
            ]
            
        except requests.RequestException as e:
            logger.error(f"Ошибка при поиске компаний: {e}")
            return []
    
    def get_vacancies_by_keyword(self, keyword: str, area: int = 1, 
                                per_page: int = 5) -> List[Dict[str, Any]]:
        """
        Поиск вакансий по ключевому слову
        
        Args:
            keyword: Ключевое слово для поиска
            area: ID региона (1 - Москва)
            per_page: Количество вакансий на страницу
            
        Returns:
            List[Dict]: Список найденных вакансий
        """
        url = f"{self.base_url}/vacancies"
        params = {
            'text': keyword,
            'area': area,
            'per_page': min(per_page, 100),
            'page': 0
        }
        
        all_vacancies = []
        
        try:
            while True:
                response = self.session.get(url, params=params)
                response.raise_for_status()
                
                data = response.json()
                vacancies = data.get('items', [])
                
                if not vacancies:
                    break
                
                # Обрабатываем каждую вакансию
                for vacancy in vacancies:
                    processed_vacancy = self._process_vacancy(vacancy)
                    if processed_vacancy:
                        all_vacancies.append(processed_vacancy)
                
                # Проверяем, есть ли еще страницы
                if params['page'] >= data.get('pages', 1) - 1:
                    break
                
                params['page'] += 1
                
                # Пауза между запросами
                time.sleep(0.25)
            
            logger.info(f"Найдено {len(all_vacancies)} вакансий по ключевому слову '{keyword}'")
            return all_vacancies
            
        except requests.RequestException as e:
            logger.error(f"Ошибка при поиске вакансий: {e}")
            return []
