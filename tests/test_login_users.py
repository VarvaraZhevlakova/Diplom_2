import allure
import requests
import pytest
from conftest import register_user_full
from urls import LOGIN_URL


class TestLogin:

    @allure.title('Проверка, система вернёт успешный ответ при правильном логине и пароле')
    def test_login_valid_credentials(self, register_user_full):
        user_data = register_user_full("user_data")

        email = user_data["user_data"]["email"]
        password = user_data["password"]

        payload = {
            "email": email,
            "password": password,
        }

        response = requests.post(LOGIN_URL, json=payload)

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

        response = requests.post(LOGIN_URL, json=payload)
        assert response.status_code == 401, f"Ожидался статус 401, получен {response.status_code}. Тело ответа: {response.text}"
        assert response.json()["message"] == expected_message, f"Ошибка: {response.json()}"


