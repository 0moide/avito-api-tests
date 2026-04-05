import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest


class TestStatistic:
    """Тесты для получения статистики (GET /api/1/statistic/{id})"""
    
    def test_get_statistic_existing_item(self, api_client, created_item):
        """TC-026: Получение статистики существующего объявления"""
        item_id = created_item["id"]
        
        response = api_client.get_statistic(item_id)
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        
        if isinstance(data, dict):
            stats = data.get("result", data)
            assert "likes" in stats or "likes" in data, "No likes field"
            assert "viewCount" in stats or "viewCount" in data, "No viewCount field"
            assert "contacts" in stats or "contacts" in data, "No contacts field"
    
    def test_get_statistic_nonexistent_item(self, api_client):
        """TC-027: Получение статистики несуществующего объявления"""
        fake_id = "00000000-0000-0000-0000-000000000000"
        
        response = api_client.get_statistic(fake_id)
        assert response.status_code == 404, f"Expected 404, got {response.status_code}"
    
    def test_get_statistic_invalid_id_format(self, api_client):
        """TC-028: Получение статистики с некорректным форматом ID"""
        invalid_id = "invalid"
        
        response = api_client.get_statistic(invalid_id)
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"