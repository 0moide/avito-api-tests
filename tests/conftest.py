import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import random
from utils.api_client import ApiClient
from utils.helpers import generate_seller_id, generate_item_name


@pytest.fixture
def api_client():
    return ApiClient("https://qa-internship.avito.com")


@pytest.fixture
def unique_seller_id():
    return generate_seller_id()


@pytest.fixture
def created_item(api_client, unique_seller_id):
    """Создает объявление перед тестом и возвращает его данные"""
    name = generate_item_name(10)
    price = random.randint(1, 10000)
    # ВАЖНО: API не принимает нули, используем значения от 1
    likes = random.randint(1, 1000)
    views = random.randint(1, 1000)
    contacts = random.randint(1, 1000)
    
    response = api_client.create_item(name, price, unique_seller_id, likes, views, contacts)
    
    if response.status_code != 200:
        pytest.skip(f"Could not create test item: {response.text}")
    
    response_data = response.json()
    item_id = api_client.parse_item_id(response_data)
    
    yield {
        "id": item_id,
        "name": name,
        "price": price,
        "seller_id": unique_seller_id,
        "likes": likes,
        "views": views,
        "contacts": contacts
    }


@pytest.fixture
def many_items_for_seller(api_client):
    """Создает 10 объявлений для одного продавца"""
    seller_id = generate_seller_id()
    items = []
    num_items = 10
    
    print(f"\n[SETUP] Creating {num_items} items for seller {seller_id}...")
    
    for i in range(num_items):
        name = generate_item_name(10)
        price = random.randint(1, 10000)
        likes = random.randint(1, 1000)
        views = random.randint(1, 1000)
        contacts = random.randint(1, 1000)
        
        response = api_client.create_item(name, price, seller_id, likes, views, contacts)
        
        if response.status_code != 200:
            print(f"[WARNING] Failed to create item {i+1}: {response.text}")
            continue
        
        response_data = response.json()
        item_id = api_client.parse_item_id(response_data)
        
        items.append({
            "id": item_id,
            "name": name,
            "price": price,
            "likes": likes,
            "views": views,
            "contacts": contacts
        })
    
    print(f"[SETUP] Successfully created {len(items)} items")
    
    yield {
        "seller_id": seller_id,
        "items": items
    }