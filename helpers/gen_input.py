from faker import Faker
import uuid


class DataGenerator:
    def __init__(self):
        self.fake = Faker('ru_RU')

    def generate_login(self):
        """Генерирует уникальный логин"""
        return f"ninja_{uuid.uuid4().hex[:8]}"

    def generate_password(self):
        """Генерирует случайный пароль"""
        return self.fake.password(length=8)

    def generate_first_name(self):
        """Генерирует случайное имя"""
        return self.fake.first_name()






