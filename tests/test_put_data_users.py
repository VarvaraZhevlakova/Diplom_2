import allure
import pytest
import requests
from conftest import api_client
from helpers.gen_input import DataGenerator


class TestPutUsersData:
    base_url = api_client.format_url("api/auth/user")

    @allure.title("Обновление данных пользователя с авторизацией")
    def test_update_user_data(self, register_and_get_user_data):
        access_token = register_and_get_user_data["access_token"]
        old_user_data = register_and_get_user_data["user_data"]

        new_name = DataGenerator().generate_first_name()
        new_email = f"{DataGenerator().generate_login()}@example.com"

        payload = {
            "name": new_name,
            "email": new_email
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": access_token
        }

        response = requests.patch(self.base_url, json=payload, headers=headers)
        response_json = response.json()

        assert response.status_code == 200, f"Ошибка: {response.status_code} - {response.text}"
        assert response_json.get("success") is True, "Ошибка: поле 'success' должно быть True"
        assert response_json.get("user", {}).get("name") == new_name, "Ошибка: имя пользователя не обновилось"
        assert response_json.get("user", {}).get("email") == new_email, "Ошибка: email пользователя не обновился"

    @allure.title("Обновление отдельных полей пользователя")
    @pytest.mark.parametrize("update_field, new_value", [
        ("name", DataGenerator().generate_first_name()),
        ("email", f"{DataGenerator().generate_login()}@example.com"),
    ])
    def test_update_specific_user_field(self, register_and_get_user_data, update_field, new_value):
        access_token = register_and_get_user_data["access_token"]

        payload = {update_field: new_value}
        headers = {
            "Content-Type": "application/json",
            "Authorization": access_token
        }

        response = requests.patch(self.base_url, json=payload, headers=headers)
        response_json = response.json()

        assert response.status_code == 200, f"Ошибка: {response.status_code} - {response.text}"
        assert response_json.get("success") is True, "Ошибка: поле 'success' должно быть True"
        assert response_json.get("user", {}).get(
            update_field) == new_value, f"Ошибка: поле {update_field} не обновилось"

    @allure.title("Попытка обновления любых данных пользователя без авторизации")
    @pytest.mark.parametrize("update_payload", [
        {"name": DataGenerator().generate_first_name()},
        {"email": f"{DataGenerator().generate_login()}@example.com"},
        {"password": DataGenerator().generate_password()},
        {"name": DataGenerator().generate_first_name(), "email": f"{DataGenerator().generate_login()}@example.com"},
        {"name": DataGenerator().generate_first_name(), "password": DataGenerator().generate_password()},
        {"email": f"{DataGenerator().generate_login()}@example.com", "password": DataGenerator().generate_password()},
        {"name": DataGenerator().generate_first_name(), "email": f"{DataGenerator().generate_login()}@example.com",
         "password": DataGenerator().generate_password()},
    ])
    def test_update_any_user_field_without_auth(self, update_payload):
        """Тест проверяет, что без авторизации обновить любое поле невозможно (ожидаем 401)"""

        url = api_client.format_url("/api/auth/user")
        headers = {"Content-Type": "application/json"}

        response = requests.patch(url, json=update_payload, headers=headers)
        response_json = response.json()

        assert response.status_code == 401, f"Ошибка: {response.status_code} - {response.text}"
        assert response_json.get("success") is False, "Ошибка: поле 'success' должно быть False"
        assert response_json.get("message") == "You should be authorised", "Ошибка: неверное сообщение об ошибке"

    @allure.title("Попытка обновления любых данных пользователя без авторизации")
    def test_update_any_user_data_without_auth(self):
        payload = {
            "name": DataGenerator().generate_first_name(),
            "email": f"{DataGenerator().generate_login()}@example.com"
        }
        headers = {"Content-Type": "application/json"}

        response = requests.patch(self.base_url, json=payload, headers=headers)
        response_json = response.json()

        assert response.status_code == 401, f"Ошибка: {response.status_code} - {response.text}"
        assert response_json.get("success") is False, "Ошибка: поле 'success' должно быть False"
        assert response_json.get("message") == "You should be authorised", "Ошибка: неверное сообщение об ошибке"
