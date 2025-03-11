import allure
import requests
from conftest import api_client

import pytest


class TestLogin:
    base_url = api_client.format_url("api/auth/login")

    @allure.title('Проверка, система вернёт успешный ответ при правильном логине и пароле')
    def test_login_valid_credentials(self, register_user_for_login):
        email = register_user_for_login['email']
        password = register_user_for_login['password']

        payload = {
            "email": email,
            "password": password,
        }

        response = requests.post(self.base_url, json=payload)

        assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}. Тело ответа: {response.text}"
        response_data = response.json()
        assert response_data["success"] is True, f"Ошибка: {response_data}"
        assert "accessToken" in response_data, "Ошибка: в ответе нет accessToken"
        assert "refreshToken" in response_data, "Ошибка: в ответе нет refreshToken"

    @allure.title('Проверка, система вернёт ошибку, если неправильно указать логин или пароль')
    @pytest.mark.parametrize(
        "login, password, expected_message",
        [
            ("incorrect_login", "incorrect_password", "email or password are incorrect"),
            ("", "valid_password", "email or password are incorrect"),
            ("valid_login", "", "email or password are incorrect")
        ]
    )
    def test_login_invalid_credentials(self, login, password, expected_message):

        payload = {
            "email": login,
            "password": password,
        }

        response = requests.post(self.base_url, json=payload)
        assert response.status_code == 401, f"Ожидался статус 401, получен {response.status_code}. Тело ответа: {response.text}"
        assert response.json()["message"] == expected_message, f"Ошибка: {response.json()}"


