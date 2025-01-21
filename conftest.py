import requests
import random
import string
import pytest
import shutil
import os
from config import URLS


# Функция для генерации случайной строки длиной 10 символов
def generate_random_string():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))


# Фикстура для создания и удаления курьера
@pytest.fixture
def create_courier():
    payload = {
        "login": generate_random_string(),
        "password": generate_random_string(),
        "firstName": generate_random_string(),
    }
    # Создание курьера
    response = requests.post(URLS.URL_COURIER, json=payload)
    assert response.status_code == 201
    assert response.json()["ok"] is True

    # Возвращаем данные курьера для использования в тесте
    yield {
        "login": payload["login"],
        "password": payload["password"]
    }

    # Логин курьера для получения ID
    login_response = requests.post(URLS.URL_COURIER_LOGIN, json={
        "login": payload["login"],
        "password": payload["password"]
    })
    if login_response.status_code == 200 and "id" in login_response.json():
        courier_id = login_response.json()["id"]

        # Удаление курьера
        delete_response = requests.delete(f"{URLS.URL_COURIER}/{courier_id}", json={"id": courier_id})
        assert delete_response.status_code == 200
        assert delete_response.json()["ok"] is True


# Хук для очистки allure_results
def pytest_sessionstart(session):
    """Очистка папки allure_results перед запуском тестов."""
    results_dir = "allure_results"
    if os.path.exists(results_dir):
        shutil.rmtree(results_dir)
    os.makedirs(results_dir)



