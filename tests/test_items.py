import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import random
from utils.helpers import generate_item_name, generate_seller_id, is_valid_uuid


class TestCreateItem:
    """Тесты для создания объявлений (POST /api/1/item)"""
    
    def test_create_item_success(self, api_client, unique_seller_id):
        name = generate_item_name(10)
        price = random.randint(1, 10000)
        likes = random.randint(1, 1000)
        views = random.randint(1, 1000)
        contacts = random.randint(1, 1000)
        
        response = api_client.create_item(name, price, unique_seller_id, likes, views, contacts)
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        data = response.json()
        item_id = api_client.parse_item_id(data)
        
        assert item_id is not None, "No ID in response"
        assert is_valid_uuid(item_id), f"Invalid UUID format: {item_id}"
    
    def test_create_item_min_name_length(self, api_client, unique_seller_id):
        name = "a"
        price = 100
        likes = 1
        views = 1
        contacts = 1
        
        response = api_client.create_item(name, price, unique_seller_id, likes, views, contacts)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    
    def test_create_item_max_name_length(self, api_client, unique_seller_id):
        name = "a" * 1000
        price = 100
        likes = 1
        views = 1
        contacts = 1
        
        response = api_client.create_item(name, price, unique_seller_id, likes, views, contacts)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    
    def test_create_item_min_price(self, api_client, unique_seller_id):
        name = generate_item_name(10)
        price = 0
        likes = 1
        views = 1
        contacts = 1
        
        response = api_client.create_item(name, price, unique_seller_id, likes, views, contacts)
        assert response.status_code == 200, f"BUG: price=0 should be accepted, got {response.status_code}"
    
    def test_create_item_max_price(self, api_client, unique_seller_id):
        name = generate_item_name(10)
        price = 999999999
        likes = 1
        views = 1
        contacts = 1
        
        response = api_client.create_item(name, price, unique_seller_id, likes, views, contacts)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    
    def test_create_item_min_seller_id(self, api_client):
        name = generate_item_name(10)
        price = 100
        seller_id = 111111
        likes = 1
        views = 1
        contacts = 1
        
        response = api_client.create_item(name, price, seller_id, likes, views, contacts)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    
    def test_create_item_max_seller_id(self, api_client):
        name = generate_item_name(10)
        price = 100
        seller_id = 999999
        likes = 1
        views = 1
        contacts = 1
        
        response = api_client.create_item(name, price, seller_id, likes, views, contacts)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    
    def test_create_item_empty_name(self, api_client, unique_seller_id):
        name = ""
        price = 100
        likes = 1
        views = 1
        contacts = 1
        
        response = api_client.create_item(name, price, unique_seller_id, likes, views, contacts)
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"
    
    def test_create_item_null_name(self, api_client, unique_seller_id):
        url = f"{api_client.base_url}/api/1/item"
        payload = {
            "sellerID": unique_seller_id,
            "name": None,
            "price": 100,
            "statistics": {
                "likes": 1,
                "viewCount": 1,
                "contacts": 1
            }
        }
        response = api_client.session.post(url, json=payload)
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"
    
    def test_create_item_negative_price(self, api_client, unique_seller_id):
        name = generate_item_name(10)
        price = -1
        likes = 1
        views = 1
        contacts = 1
        
        response = api_client.create_item(name, price, unique_seller_id, likes, views, contacts)
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"
    
    def test_create_item_price_as_string(self, api_client, unique_seller_id):
        url = f"{api_client.base_url}/api/1/item"
        payload = {
            "sellerID": unique_seller_id,
            "name": generate_item_name(10),
            "price": "сто",
            "statistics": {
                "likes": 1,
                "viewCount": 1,
                "contacts": 1
            }
        }
        response = api_client.session.post(url, json=payload)
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"
    
    def test_create_item_seller_id_out_of_range(self, api_client):
        name = generate_item_name(10)
        price = 100
        seller_id = 1
        likes = 1
        views = 1
        contacts = 1
        
        response = api_client.create_item(name, price, seller_id, likes, views, contacts)
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"
    
    def test_create_item_seller_id_as_string(self, api_client):
        url = f"{api_client.base_url}/api/1/item"
        payload = {
            "sellerID": "abc",
            "name": generate_item_name(10),
            "price": 100,
            "statistics": {
                "likes": 1,
                "viewCount": 1,
                "contacts": 1
            }
        }
        response = api_client.session.post(url, json=payload)
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"
    
    def test_create_item_missing_name_field(self, api_client, unique_seller_id):
        url = f"{api_client.base_url}/api/1/item"
        payload = {
            "sellerID": unique_seller_id,
            "price": 100,
            "statistics": {
                "likes": 1,
                "viewCount": 1,
                "contacts": 1
            }
        }
        response = api_client.session.post(url, json=payload)
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"
    
    def test_create_item_missing_statistics_field(self, api_client, unique_seller_id):
        url = f"{api_client.base_url}/api/1/item"
        payload = {
            "sellerID": unique_seller_id,
            "name": generate_item_name(10),
            "price": 100
        }
        response = api_client.session.post(url, json=payload)
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"
    
    def test_create_item_idempotency(self, api_client, unique_seller_id):
        name = generate_item_name(10)
        price = 100
        likes = 1
        views = 1
        contacts = 1
        
        response1 = api_client.create_item(name, price, unique_seller_id, likes, views, contacts)
        response2 = api_client.create_item(name, price, unique_seller_id, likes, views, contacts)
        
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        id1 = api_client.parse_item_id(response1.json())
        id2 = api_client.parse_item_id(response2.json())
        
        assert id1 != id2, "Two identical requests should create different items"


class TestGetItemById:
    """Тесты для получения объявления по ID (GET /api/1/item/{id})"""
    
    def test_get_existing_item(self, api_client, created_item):
        item_id = created_item["id"]
        
        response = api_client.get_item_by_id(item_id)
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        
        if isinstance(data, list) and len(data) > 0:
            item = data[0] if isinstance(data[0], dict) else data[0][0]
        elif isinstance(data, dict):
            item = data
        else:
            pytest.fail(f"Unexpected response structure: {data}")
        
        assert item["id"] == item_id, f"Expected {item_id}, got {item['id']}"
        assert item["name"] == created_item["name"], "Name mismatch"
        assert item["price"] == created_item["price"], "Price mismatch"
        assert item["sellerId"] == created_item["seller_id"], "SellerId mismatch"
    
    def test_get_nonexistent_item(self, api_client):
        fake_id = "00000000-0000-0000-0000-000000000000"
        
        response = api_client.get_item_by_id(fake_id)
        assert response.status_code == 404, f"Expected 404, got {response.status_code}"
    
    def test_get_item_invalid_id_format(self, api_client):
        invalid_id = "123"
        
        response = api_client.get_item_by_id(invalid_id)
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"
    
    def test_get_item_empty_id(self, api_client):
        response = api_client.get_item_by_id("")
        assert response.status_code in [400, 404], f"Expected 400 or 404, got {response.status_code}"


class TestGetItemsBySeller:
    """Тесты для получения объявлений по ID продавца (GET /api/1/{sellerId}/item)"""
    
    def test_get_items_existing_seller(self, api_client, unique_seller_id):
        items = []
        for i in range(3):
            name = generate_item_name(10)
            price = random.randint(1, 10000)
            likes = random.randint(1, 1000)
            views = random.randint(1, 1000)
            contacts = random.randint(1, 1000)
            
            response = api_client.create_item(name, price, unique_seller_id, likes, views, contacts)
            assert response.status_code == 200, f"Failed to create item {i+1}"
            items.append(response.json())
        
        response = api_client.get_items_by_seller(unique_seller_id)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        
        if isinstance(data, list) and len(data) > 0 and isinstance(data[0], list):
            items_data = data[0]
        else:
            items_data = data
        
        assert len(items_data) >= 3, f"Expected at least 3 items, got {len(items_data)}"
    
    def test_get_items_seller_without_items(self, api_client):
        seller_id = generate_seller_id()
        
        response = api_client.get_items_by_seller(seller_id)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        
        if isinstance(data, list):
            if len(data) > 0 and isinstance(data[0], list):
                assert len(data[0]) == 0, "Expected empty list"
            else:
                assert len(data) == 0, "Expected empty list"
    
    def test_get_items_seller_id_out_of_range(self, api_client):
        seller_id = 1
        
        response = api_client.get_items_by_seller(seller_id)
        assert response.status_code == 400, f"BUG: Expected 400, got {response.status_code}"
    
    def test_get_items_seller_id_as_string(self, api_client):
        url = f"{api_client.base_url}/api/1/abc/item"
        response = api_client.session.get(url)
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"
    
    def test_get_items_negative_seller_id(self, api_client):
        seller_id = -1
        
        response = api_client.get_items_by_seller(seller_id)
        assert response.status_code == 400, f"BUG: Expected 400, got {response.status_code}"