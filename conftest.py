import random

import pytest
import requests

from api_client import ApiClient
from helpers.gen_input import DataGenerator
from urls import BASE_URL_BURGERS, INGREDIENTS_URL, REGISTER_URL, USER_URL


@pytest.fixture
def api_client():
    return ApiClient(base_url=BASE_URL_BURGERS)


@pytest.fixture
def get_ingredients():
    response = requests.get(INGREDIENTS_URL)
    return response.json().get('data', [])


@pytest.fixture
def random_ingredient(get_ingredients):
    ingredients = get_ingredients
    return random.choice(ingredients)


@pytest.fixture
def register_user():
    data_generator = DataGenerator()
    name = data_generator.generate_first_name()
    email = f"{data_generator.generate_login()}@example.com"
    password = data_generator.generate_password()

    payload = {
        "email": email,
        "password": password,
        "name": name
    }
    response = requests.post(REGISTER_URL, json=payload)
    return response


@pytest.fixture
def register_user_full():
    def _register_user(return_type="default"):
        data_generator = DataGenerator()
        name = data_generator.generate_first_name()
        email = f"{data_generator.generate_login()}@example.com"
        password = data_generator.generate_password()

        payload = {
            "email": email,
            "password": password,
            "name": name
        }
        response = requests.post(REGISTER_URL, json=payload)

        response_data = response.json()
        access_token = response_data.get("accessToken")

        if return_type == "login":
            return {
                "response": response,
                "email": email,
                "password": password
            }
        elif return_type == "orders":
            return access_token
        elif return_type == "user_data":
            headers = {
                "Content-Type": "application/json",
                "Authorization": access_token
            }
            response_user = requests.get(USER_URL, headers=headers)
            user_data = response_user.json().get("user", {})

            return {
                "access_token": access_token,
                "user_data": user_data,
                "password": password
            }

        return response

    return _register_user


@pytest.fixture
def delete_user():
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.delete(USER_URL, headers=headers)
    return response

