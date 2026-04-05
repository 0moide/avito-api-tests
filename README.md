# Автотесты для API микросервиса объявлений Avito

## Описание

Автоматизированные тесты для проверки API микросервиса объявлений Avito.

**Базовый URL**: `https://qa-internship.avito.com`

**Тестируемые методы API**:
- `POST /api/1/item` — создание объявления
- `GET /api/1/item/{id}` — получение объявления по ID
- `GET /api/1/{sellerId}/item` — получение объявлений по ID продавца
- `GET /api/1/statistic/{id}` — получение статистики по объявлению

## Структура проекта

avito-api-tests/
│
├── tests/
│ ├── conftest.py
│ ├── test_items.py
│ ├── test_statistic.py
│ └── test_functional.py
│
├── utils/
│ ├── api_client.py
│ └── helpers.py
│
├── requirements.txt # Зависимости Python
├── TESTCASES.md # Документация тест-кейсов
├── BUGS.md # Отчет о найденных багах
└── README.md


## Требования

- **Python**: версия 3.8 или выше
- **Операционная система**: Windows / macOS / Linux
- **Доступ в интернет**: для отправки запросов к API

## Установка зависимостей

pip install -r requirements.txt

## Запуск всех тестов

pytest tests/ -v

## Запуск конкретного файла с тестами

pytest tests/test_items.py -v
pytest tests/test_statistic.py -v
pytest tests/test_functional.py -v