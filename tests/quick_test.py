# quick_test.py
import requests

url = "https://qa-internship.avito.com/api/1/item"

# Тест с null вместо 0
payload = {
    "sellerID": 123456,
    "name": "Test Null",
    "price": 100,
    "statistics": {
        "likes": None,
        "viewCount": None,
        "contacts": None
    }
}

print(f"Отправляем: {payload}")
response = requests.post(url, json=payload)
print(f"Статус: {response.status_code}")
print(f"Ответ: {response.text}")

# Тест без поля statistics
payload2 = {
    "sellerID": 123456,
    "name": "Test No Stats",
    "price": 100
}

print(f"\nОтправляем: {payload2}")
response = requests.post(url, json=payload2)
print(f"Статус: {response.status_code}")
print(f"Ответ: {response.text}")