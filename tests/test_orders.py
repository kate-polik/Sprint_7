import pytest
import requests
import allure
from utils.helpers import generate_random_string
from config import URLS


@allure.feature('Управление заказами')
class TestOrders:
    @allure.story('Создание заказа')
    @allure.title('Создание заказа с цветами: {colors}')
    @pytest.mark.parametrize("colors", [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"],
        [],
    ])
    # Тест создания заказов с разными цветами
    def test_create_order(self, colors):
        with allure.step('Подготавливаем данные для создания заказа'):
            payload = {
                "firstName": generate_random_string(),
                "lastName": generate_random_string(),
                "address": "ул. Сеньора Помидора, 100500",
                "metroStation": 1,
                "phone": "+7 789 999 45 85",
                "rentTime": 5,
                "deliveryDate": "2025-01-25",
                "comment": "Тестовый комент",
                "color": colors,
            }

        with allure.step('Отправляем POST-запрос на создание заказа'):
            response = requests.post(URLS.URL_ORDERS, json=payload)

        with allure.step('Проверяем, что код ответа равен 201'):
            assert response.status_code == 201, f"Ошибка создания заказа: {response.status_code}"

        with allure.step('Проверяем наличие номера заказа (track) в ответе'):
            assert "track" in response.json(), "В ответе отсутствует track"

    @allure.story('Получение заказов')
    @allure.title('Получение списка заказов')
    # Тест получения списка заказов с фильтрацией
    def test_get_orders(self):
        with allure.step('Подготавливаем параметры запроса'):
            params = {
                "nearestStation": '["1","2","3"]',  # Станции метро
                "limit": 4,  # Количество заказов на странице
                "page": 2  # Номер страницы (3я страница)
            }

        with allure.step('Отправляем GET-запрос на получение списка заказов'):
            response = requests.get(URLS.URL_ORDERS, params=params)

        with allure.step('Проверяем, что код ответа равен 200'):
            assert response.status_code == 200, f"Ожидался статус 200, но получен {response.status_code}"

        with allure.step('Получаем данные из ответа'):
            response_data = response.json()

        with allure.step('Проверяем структуру ответа'):
            assert "orders" in response_data, "Ответ не содержит ключа 'orders'"
            assert isinstance(response_data["orders"], list), "Значение 'orders' не является списком"
