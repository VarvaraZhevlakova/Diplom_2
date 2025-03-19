import allure
import requests
from conftest import delete_user
from helpers.gen_input import DataGenerator
from urls import REGISTER_URL


class TestPostUser:

    @allure.title('Создание уникального пользователя ')
    def test_register_user(self, delete_user):
        data_generator = DataGenerator()
        name = data_generator.generate_first_name()
        email = f"{data_generator.generate_login()}@example.com"
        password = data_generator.generate_password()

        register_data = {
            "email": email,
            "password": password,
            "name": name
        }

        register_response = requests.post(REGISTER_URL, json=register_data)
        assert register_response.status_code == 200, f"Ошибка регистрации: {register_response.status_code} - {register_response.text}"
        register_response_json = register_response.json()
        assert register_response_json["success"] is True, "Регистрация не удалась"

        delete_response = delete_user
        response_json = delete_response.json()
        assert response_json.get("success") is False, "Ошибка: поле 'success' должно быть False"

    @allure.title('Попытка регистрации уже существующего пользователя')
    def test_register_existing_user(self):
        data_generator = DataGenerator()
        name = data_generator.generate_first_name()
        email = f"{data_generator.generate_login()}@example.com"
        password = data_generator.generate_password()

        register_data = {
            "email": email,
            "password": password,
            "name": name
        }

        register_response = requests.post(REGISTER_URL, json=register_data)

        assert register_response.status_code == 200, f"Ошибка регистрации: {register_response.status_code} - {register_response.text}"
        register_response_json = register_response.json()
        assert register_response_json["success"] is True, "Регистрация первого пользователя не удалась"

        #попытка зарегаться под юзером, который уже зареган
        register_response_already_exist = requests.post(REGISTER_URL, json=register_data)

        assert register_response_already_exist.status_code == 403, f"Ожидался статус 403, получен {register_response_already_exist.status_code}. Тело ответа: {register_response_already_exist.text}"
        register_response_already_exist_json = register_response_already_exist.json()
        assert register_response_already_exist_json["success"] is False, "Ответ не содержит поле 'success' со значением False"
        assert register_response_already_exist_json["message"] == "User already exists", f"Ошибка: {register_response_already_exist_json}"

    @allure.title('Создание пользователя без одного из обязательных полей')
    def test_register_user_missing_field(self):
        data_generator = DataGenerator()
        name = data_generator.generate_first_name()
        email = f"{data_generator.generate_login()}@example.com"
        password = data_generator.generate_password()

        invalid_payloads = [
            {"password": password, "name": name},
            {"email": email, "name": name},
            {"email": email, "password": password}
        ]

        for payload in invalid_payloads:
            response = requests.post(REGISTER_URL, json=payload)

            assert response.status_code == 403, f"Ошибка: ожидался код 403, но получен {response.status_code} - {response.text}"
            response_json = response.json()

            assert response_json["success"] is False, "Ошибка: поле 'success' должно быть False"
            assert response_json["message"] == "Email, password and name are required fields", f"Ошибка: неверное сообщение об ошибке: {response_json.get('message')}"

