import requests
import pytest
import allure
from config import URLS
from conftest import generate_random_string


@allure.feature('Управление курьерами')
class TestCourierCreate:
    @allure.story('Создание курьера')
    @allure.title('Успешное создание курьера')
    # Тест успешного создания курьера
    def test_create_courier_success(self, create_courier):
        with allure.step('Получаем данные курьера из фикстуры'):
            courier_data = create_courier

        with allure.step('Подготавливаем данные для входа'):
            login_payload = {
                "login": courier_data["login"],
                "password": courier_data["password"]
            }

        with allure.step('Отправляем POST-запрос для входа курьера'):
            login_response = requests.post(URLS.URL_COURIER_LOGIN, json=login_payload)

        with allure.step('Проверяем, что код ответа равен 200'):
            assert login_response.status_code == 200

        with allure.step('Проверяем, что в ответе содержится ID курьера'):
            assert "id" in login_response.json(), "ID не найден в ответе на логин"

    @allure.story('Создание курьера')
    @allure.title('Попытка создать курьера с существующим логином')
    # Тест попытки создать курьера с дублирующимся логином
    def test_create_duplicate_couriers(self):
        with allure.step('Подготавливаем тестовые данные'):
            payload = {
                "login": generate_random_string(),
                "password": generate_random_string(),
                "firstName": generate_random_string(),
            }

        with allure.step('Создаем первого курьера'):
            requests.post(URLS.URL_COURIER, json=payload)

        with allure.step('Пытаемся создать дубликат курьера'):
            response = requests.post(URLS.URL_COURIER, json=payload)

        with allure.step('Проверяем, что код ответа равен 409'):
            assert response.status_code == 409

        with allure.step('Проверяем сообщение об ошибке'):
            assert response.json()['message'] == "Этот логин уже используется. Попробуйте другой."

    @allure.story('Создание курьера')
    @allure.title('Создание курьера с отсутствующими обязательными полями: {missing_fields}')
    @pytest.mark.parametrize(
        "missing_fields, expected_message",
        [
            (["login"], "Недостаточно данных для создания учетной записи"),
            (["password"], "Недостаточно данных для создания учетной записи"),
            (["login", "password"], "Недостаточно данных для создания учетной записи"),
        ]
    )
    # Тест создания курьера с отсутствующими обязательными полями
    def test_create_courier_missing_fields(self, missing_fields, expected_message):
        with allure.step('Подготавливаем тестовые данные'):
            payload = {
                "login": generate_random_string(),
                "password": generate_random_string(),
                "firstName": generate_random_string(),
            }

        with allure.step(f'Удаляем поля: {missing_fields}'):
            for field in missing_fields:
                del payload[field]

        with allure.step('Отправляем POST-запрос на создание курьера'):
            response = requests.post(URLS.URL_COURIER, json=payload)

        with allure.step('Проверяем, что код ответа равен 400'):
            assert response.status_code == 400

        with allure.step('Проверяем сообщение об ошибке'):
            response_body = response.json()
            assert response_body["message"] == expected_message
