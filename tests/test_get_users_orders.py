import allure
import pytest
import requests
from urls import ORDER_URL
from conftest import register_user_full


class TestGetUsersOrders:

    @allure.title('Получение заказов пользователя без авторизации')
    def test_get_user_orders_without_auth(self):
        response = requests.get(ORDER_URL)

        assert response.status_code == 401, f"Ошибка: ожидался код 401, но получен {response.status_code} - {response.text}"

        response_json = response.json()
        assert response_json["success"] is False, "Ошибка: поле 'success' должно быть False"
        assert response_json["message"] == "You should be authorised", f"Ошибка: неверное сообщение об ошибке: {response_json.get('message')}"

    @pytest.mark.usefixtures("register_user_full")
    @allure.title('Получение заказов пользователя с авторизацией')
    def test_get_user_orders_with_auth(self, register_user_full):
        access_token = register_user_full("orders")

        headers = {
            "Content-Type": "application/json",
            "Authorization": access_token
        }

        response = requests.get(ORDER_URL, headers=headers)

        assert response.status_code == 200, f"Ошибка: ожидался код 200, но получен {response.status_code} - {response.text}"
        response_json = response.json()
        assert response_json["success"] is True, "Ошибка: поле 'success' должно быть True"
        assert "orders" in response_json, "Ошибка: в ответе отсутствует ключ 'orders'"
        assert isinstance(response_json["orders"], list), "Ошибка: 'orders' должен быть списком"

