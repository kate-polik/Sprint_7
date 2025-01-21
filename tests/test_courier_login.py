import pytest
import requests
import allure
from utils.helpers import generate_random_string
from config import URLS


class TestCourierLogin:

    @allure.story("Успешный логин курьера")
    @allure.title('Вход с корректными данными')
    # Тест успешного логина курьера с использованием фикстуры
    def test_courier_login_success(self, create_courier):
        # Получаем данные созданного курьера из фикстуры
        courier_data = create_courier
        login_payload = {
            "login": courier_data["login"],
            "password": courier_data["password"],
        }

        with allure.step("Отправка запроса на логин курьера"):
            response = requests.post(URLS.URL_COURIER_LOGIN, json=login_payload)

        with allure.step("Проверка успешного логина курьера"):
            assert response.status_code == 200, "Неверный статус ответа"
            response_body = response.json()
            assert "id" in response_body, "ID не найден в ответе на логин"

    @allure.story('Неуспешная авторизация')
    @allure.title('Попытка входа с невалидными данными: {test_case}')
    @pytest.mark.parametrize('test_case, credentials, expected_status, expected_message', [
        ('неверный пароль',
         lambda x: {"login": x["login"], "password": generate_random_string()},
         404, "Учетная запись не найдена"),
        ('неверный логин',
         lambda x: {"login": generate_random_string(), "password": x["password"]},
         404, "Учетная запись не найдена"),
        ('случайные логин и пароль',
         lambda x: {"login": generate_random_string(), "password": generate_random_string()},
         404, "Учетная запись не найдена"),
        ('отсутствует логин',
         lambda x: {"login": "", "password": x["password"]},
         400, "Недостаточно данных для входа"),
        ('отсутствует пароль',
         lambda x: {"login": x["login"], "password": ""},
         400, "Недостаточно данных для входа")
    ])
    # Проверка различных сценариев неуспешной авторизации курьера
    def test_login_negative_cases(self, create_courier, test_case, credentials, expected_status, expected_message):
        with allure.step(f'Подготовка тестовых данных для сценария: {test_case}'):
            # Получаем тестовые данные, используя lambda-функцию из параметризации
            payload = credentials(create_courier)

        with allure.step('Отправляем POST-запрос для авторизации курьера'):
            response = requests.post(URLS.URL_COURIER_LOGIN, json=payload)

        with allure.step(f'Проверяем код ответа {expected_status}'):
            assert response.status_code == expected_status, \
                f"Ожидался код ответа {expected_status}, получен {response.status_code}"

        with allure.step('Проверяем сообщение об ошибке'):
            assert response.json()["message"] == expected_message, \
                f"Неожиданное сообщение об ошибке: {response.json()['message']}"
