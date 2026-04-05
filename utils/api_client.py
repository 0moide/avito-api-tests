import requests
from typing import Optional, Dict, Any


class ApiClient:
    """HTTP клиент для работы с API"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
    
    def create_item(self, name: str, price: int, seller_id: int, 
                    likes: int = 0, views: int = 0, contacts: int = 0) -> Dict[str, Any]:
        """
        Создание объявления
        Правильный формат из Postman-коллекции:
        {
            "sellerID": <integer>,
            "name": <string>,
            "price": <integer>,
            "statistics": {
                "likes": <integer>,
                "viewCount": <integer>,
                "contacts": <integer>
            }
        }
        """
        url = f"{self.base_url}/api/1/item"
        
        payload = {
            "sellerID": seller_id,
            "name": name,
            "price": price,
            "statistics": {
                "likes": likes,
                "viewCount": views,
                "contacts": contacts
            }
        }
        
        response = self.session.post(url, json=payload)
        return response
    
    def get_item_by_id(self, item_id: str) -> Dict[str, Any]:
        """Получение объявления по ID"""
        url = f"{self.base_url}/api/1/item/{item_id}"
        response = self.session.get(url)
        return response
    
    def get_items_by_seller(self, seller_id: int) -> Dict[str, Any]:
        """Получение объявлений по ID продавца"""
        url = f"{self.base_url}/api/1/{seller_id}/item"
        response = self.session.get(url)
        return response
    
    def get_statistic(self, item_id: str) -> Dict[str, Any]:
        """Получение статистики по объявлению"""
        url = f"{self.base_url}/api/1/statistic/{item_id}"
        response = self.session.get(url)
        return response
    
    def parse_item_id(self, response_data) -> Optional[str]:
        """Извлечение ID объявления из ответа"""
        if isinstance(response_data, dict):
            return response_data.get("id")
        elif isinstance(response_data, list) and len(response_data) > 0:
            if isinstance(response_data[0], dict):
                return response_data[0].get("id")
        return None