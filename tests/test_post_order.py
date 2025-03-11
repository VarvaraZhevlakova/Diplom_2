import allure
import pytest
import requests
from conftest import api_client


class TestOrders:
    base_url = api_client.format_url("api/orders")

    @allure.title("Проверка успешного создания заказа без авторизации")
    def test_create_order_success(self, random_ingredient):
        payload = {"ingredients": [random_ingredient, random_ingredient]}
        response = requests.post(self.base_url, json=payload, headers={"Content-Type": "application/json"})

        assert response.status_code == 200, f"Ошибка: {response.status_code}, тело ответа: {response.text}"
        response_json = response.json()
        assert response_json["success"] is True, "Ошибка: заказ не был создан"
        assert "order" in response_json and "number" in response_json["order"], "Ошибка: номер заказа отсутствует"

    @pytest.mark.usefixtures("register_user")
    @allure.title("Проверка успешного создания заказа с авторизацией пользователя")
    def test_create_order_with_registration(self, register_user, random_ingredient):

        access_token = register_user.json().get("accessToken")

        payload = {"ingredients": [random_ingredient, random_ingredient]}
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        }
        response = requests.post(self.base_url, json=payload, headers={"Content-Type": "application/json"})
        assert response.status_code == 200, f"Ошибка: {response.status_code}, тело ответа: {response.text}"
        response_json = response.json()
        assert response_json["success"] is True, "Ошибка: заказ не был создан"
        assert "order" in response_json and "number" in response_json["order"], "Ошибка: номер заказа отсутствует"

    @allure.title("Проверка ошибки при отсутствии ингредиентов в заказе")
    def test_create_order_no_ingredients(self):
        payload = {"ingredients": []}
        response = requests.post(self.base_url, json=payload)

        assert response.status_code == 400, f"Ошибка: {response.status_code}, тело ответа: {response.text}"
        response_json = response.json()
        assert response_json["success"] is False, "Ошибка: заказ без ингредиентов не должен быть успешным"
        assert response_json["message"] == "Ingredient ids must be provided", "Ошибка: сообщение не совпадает"

    @allure.title("Проверка ошибки с неверных хешем ингредиента")
    def test_create_order_invalid_ingredient(self):
        payload = {"ingredients": ["invalid_ingredient"]}
        response = requests.post(self.base_url, json=payload)

        assert response.status_code == 500, f"Ошибка: {response.status_code}, тело ответа: {response.text}"





