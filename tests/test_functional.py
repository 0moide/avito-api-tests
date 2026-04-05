import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import random
import time
from utils.helpers import generate_seller_id, generate_item_name


class TestFunctionalChecks:
    """Функциональные проверки"""
    
    def test_unique_item_ids(self, api_client, unique_seller_id):
        ids = []
        
        for i in range(10):
            name = generate_item_name(10)
            price = random.randint(1, 10000)
            likes = random.randint(1, 1000)
            views = random.randint(1, 1000)
            contacts = random.randint(1, 1000)
            
            response = api_client.create_item(name, price, unique_seller_id, likes, views, contacts)
            assert response.status_code == 200, f"Failed to create item {i+1}: {response.text}"
            
            item_id = api_client.parse_item_id(response.json())
            assert item_id is not None, f"No ID in response for item {i+1}"
            ids.append(item_id)
        
        unique_ids = set(ids)
        assert len(ids) == len(unique_ids), f"Duplicate IDs found"
    
    def test_response_structure_create_item(self, api_client, unique_seller_id):
        name = generate_item_name(10)
        price = 100
        likes = 1
        views = 1
        contacts = 1
        
        response = api_client.create_item(name, price, unique_seller_id, likes, views, contacts)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        assert "id" in data, "Response missing 'id' field"
        assert isinstance(data["id"], str), "id should be string"
    
    def test_response_structure_get_item(self, api_client, created_item):
        item_id = created_item["id"]
        
        response = api_client.get_item_by_id(item_id)
        assert response.status_code == 200
        
        data = response.json()
        
        if isinstance(data, list) and len(data) > 0:
            item = data[0] if isinstance(data[0], dict) else data[0][0]
        elif isinstance(data, dict):
            item = data
        else:
            pytest.fail(f"Unexpected response structure")
        
        expected_fields = ["id", "name", "price", "sellerId", "statistics"]
        for field in expected_fields:
            assert field in item, f"Missing '{field}' field"
    
    def test_response_structure_statistic(self, api_client, created_item):
        item_id = created_item["id"]
        
        response = api_client.get_statistic(item_id)
        assert response.status_code == 200
        
        data = response.json()
        
        if isinstance(data, dict):
            stats = data.get("result", data)
            expected_fields = ["likes", "viewCount", "contacts"]
            for field in expected_fields:
                assert field in stats or field in data, f"Missing '{field}' field"
    
    def test_performance_create_items(self, api_client, unique_seller_id):
        start_time = time.time()
        
        for i in range(100):
            name = generate_item_name(10)
            price = random.randint(1, 10000)
            likes = random.randint(1, 1000)
            views = random.randint(1, 1000)
            contacts = random.randint(1, 1000)
            
            response = api_client.create_item(name, price, unique_seller_id, likes, views, contacts)
            assert response.status_code == 200, f"Failed at item {i+1}: {response.text}"
        
        end_time = time.time()
        total_time = end_time - start_time
        avg_time = total_time / 100
        
        print(f"\nTotal time for 100 items: {total_time:.2f} seconds")
        print(f"Average time per item: {avg_time:.3f} seconds")
        
        assert avg_time < 2, f"Average response time {avg_time:.2f}s > 2s"
    
    def test_sql_injection(self, api_client, unique_seller_id):
        malicious_names = [
            "'; DROP TABLE items; --",
            "' OR '1'='1",
            "'; UPDATE items SET price = 0; --",
            "1; DELETE FROM items; --"
        ]
        
        for malicious_name in malicious_names:
            response = api_client.create_item(malicious_name, 100, unique_seller_id, 1, 1, 1)
            assert response.status_code in [200, 400], f"Failed for name: {malicious_name}"
    
    def test_xss_prevention(self, api_client, unique_seller_id):
        xss_payloads = [
            "<script>alert('xss')</script>",
            "<img src=x onerror=alert('xss')>",
            "javascript:alert('xss')",
            "<iframe src='javascript:alert(\"xss\")'>"
        ]
        
        for payload in xss_payloads:
            response = api_client.create_item(payload, 100, unique_seller_id, 1, 1, 1)
            assert response.status_code in [200, 400], f"Failed for payload: {payload}"


class TestLoadTests:
    """Нагрузочные тесты"""
    
    def test_load_get_items_by_seller(self, api_client):
        seller_id = generate_seller_id()
        
        print(f"\nCreating 100 items for seller {seller_id}...")
        for i in range(100):
            name = generate_item_name(10)
            price = random.randint(1, 10000)
            likes = random.randint(1, 1000)
            views = random.randint(1, 1000)
            contacts = random.randint(1, 1000)
            
            response = api_client.create_item(name, price, seller_id, likes, views, contacts)
            assert response.status_code == 200, f"Failed to create item {i+1}: {response.text}"
        
        start_time = time.time()
        response = api_client.get_items_by_seller(seller_id)
        end_time = time.time()
        
        load_time = end_time - start_time
        
        print(f"\nTime to get 100 items: {load_time:.2f} seconds")
        
        assert response.status_code == 200
        assert load_time < 3, f"Load time {load_time:.2f}s > 3s"