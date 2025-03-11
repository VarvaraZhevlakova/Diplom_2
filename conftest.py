import random

import pytest
import requests
from urls import base_url_burgers
from helpers.gen_input import DataGenerator


class ApiClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def format_url(self, endpoint):
        return f"{self.base_url}{endpoint}"


api_client = ApiClient(base_url_burgers)


@pytest.fixture
def get_ingredients():
    url = api_client.format_url("api/ingredients")
    response = requests.get(url)
    return response.json().get('data', [])


@pytest.fixture
def random_ingredient(get_ingredients):
    ingredients = get_ingredients
    return random.choice(ingredients)


@pytest.fixture
def register_user():
    url = api_client.format_url("api//auth/register")
    data_generator = DataGenerator()
    name = data_generator.generate_first_name()
    email = f"{data_generator.generate_login()}@example.com"
    password = data_generator.generate_password()

    payload = {
        "email": email,
        "password": password,
        "name": name
    }
    response = requests.post(api_client.format_url("/api/auth/register"), json=payload)
    return response


@pytest.fixture
def register_user_for_login():
    url = api_client.format_url("api/auth/register")
    data_generator = DataGenerator()
    name = data_generator.generate_first_name()
    email = f"{data_generator.generate_login()}@example.com"
    password = data_generator.generate_password()

    payload = {
        "email": email,
        "password": password,
        "name": name
    }
    response = requests.post(api_client.format_url("/api/auth/register"), json=payload)

    return {
        "response": response,
        "email": email,
        "password": password
    }


@pytest.fixture
def register_user_for_get_orders():
    url = api_client.format_url("api/auth/register")
    data_generator = DataGenerator()

    name = data_generator.generate_first_name()
    email = f"{data_generator.generate_login()}@example.com"
    password = data_generator.generate_password()

    payload = {
        "email": email,
        "password": password,
        "name": name
    }
    response = requests.post(url, json=payload)

    response_json = response.json()
    return response_json["accessToken"]


@pytest.fixture
def register_and_get_user_data():

    url_register = api_client.format_url("/api/auth/register")
    data_generator = DataGenerator()
    name = data_generator.generate_first_name()
    email = f"{data_generator.generate_login()}@example.com"
    password = data_generator.generate_password()

    payload = {
        "email": email,
        "password": password,
        "name": name
    }
    response = requests.post(url_register, json=payload)
    response_data = response.json()

    access_token = response_data.get("accessToken")
    url_user_data = api_client.format_url("/api/auth/user")
    headers = {
        "Content-Type": "application/json",
        "Authorization": access_token
    }

    response_user = requests.get(url_user_data, headers=headers)
    user_data = response_user.json()

    return {
        "access_token": access_token,
        "user_data": user_data
    }


@pytest.fixture
def delete_user():
    url = api_client.format_url("/api/auth/user")
    headers = {
        "Content-Type": "application/json"}

    response = requests.delete(url, headers=headers)
    return response

