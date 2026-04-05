import random
import uuid
from typing import List, Optional


def generate_seller_id() -> int:
    """Генерация уникального sellerId в диапазоне 111111-999999"""
    return random.randint(111111, 999999)


def generate_item_name(length: int = 10) -> str:
    """Генерация имени объявления"""
    letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return ''.join(random.choice(letters) for _ in range(length))


def is_valid_uuid(value: str) -> bool:
    """Проверка, является ли строка валидным UUID"""
    try:
        uuid.UUID(value)
        return True
    except ValueError:
        return False


def extract_ids_from_response(response_data) -> List[str]:
    """Извлечение всех ID из ответа"""
    ids = []
    
    if isinstance(response_data, list):
        if len(response_data) > 0 and isinstance(response_data[0], list):
            for sublist in response_data:
                if isinstance(sublist, list):
                    ids.extend([item.get("id") for item in sublist if item.get("id")])
        else:
            ids = [item.get("id") for item in response_data if item.get("id")]
    elif isinstance(response_data, dict):
        if "id" in response_data:
            ids.append(response_data["id"])
        elif "result" in response_data and isinstance(response_data["result"], dict):
            if "id" in response_data["result"]:
                ids.append(response_data["result"]["id"])
    
    return ids