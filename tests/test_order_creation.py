import requests
import random
import string

BASE_URL = 'https://stellarburgers.nomoreparties.site'


def generate_unique_email():
    """Генерирует случайный уникальный email."""
    return ''.join(random.choices(string.ascii_lowercase, k=10)) + '@example.com'


class TestOrderCreation:

    def get_ingredients(self):
        """Получает список ингредиентов."""
        response = requests.get(f'{BASE_URL}/api/ingredients')
        assert response.status_code == 200, f"Failed to get ingredients: {response.text}"
        ingredients = [item['_id'] for item in response.json()['data']]
        return ingredients

    def test_create_order_authorized(self):
        """Создание заказа с авторизацией и ингредиентами."""
        # Создаём пользователя с уникальным email
        email = generate_unique_email()
        data = {
            'email': email,
            'password': 'password123',
            'name': 'OrderUser'
        }
        response = requests.post(f'{BASE_URL}/api/auth/register', json=data)
        assert response.status_code == 200, f"Registration failed: {response.text}"
        access_token = response.json().get('accessToken')
        assert access_token, "No accessToken in response."
        headers = {'Authorization': access_token}

        # Получаем ингредиенты
        ingredients = self.get_ingredients()

        order_data = {
            'ingredients': ingredients
        }

        # Создаём заказ
        response = requests.post(f'{BASE_URL}/api/orders', headers=headers, json=order_data)
        assert response.status_code == 200, f"Order creation failed: {response.text}"
        assert response.json()['success'] is True

        # Удаляем пользователя после теста
        requests.delete(f'{BASE_URL}/api/auth/user', headers=headers)

    def test_create_order_unauthorized(self):
        """Создание заказа без авторизации (разрешено)."""
        # Получаем ингредиенты
        ingredients = self.get_ingredients()

        order_data = {
            'ingredients': ingredients
        }

        # Пытаемся создать заказ без токена
        response = requests.post(f'{BASE_URL}/api/orders', json=order_data)
        # Ожидаем, что заказ будет успешно создан
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        assert response.json()['success'] is True

    def test_create_order_no_ingredients(self):
        """Создание заказа без ингредиентов."""
        # Создаём пользователя с уникальным email
        email = generate_unique_email()
        data = {
            'email': email,
            'password': 'password123',
            'name': 'OrderUser2'
        }
        response = requests.post(f'{BASE_URL}/api/auth/register', json=data)
        assert response.status_code == 200, f"Registration failed: {response.text}"
        access_token = response.json().get('accessToken')
        assert access_token, "No accessToken in response."
        headers = {'Authorization': access_token}

        order_data = {
            'ingredients': []
        }

        # Пытаемся создать заказ с пустым списком ингредиентов
        response = requests.post(f'{BASE_URL}/api/orders', headers=headers, json=order_data)
        assert response.status_code == 400, f"Expected 400, got {response.status_code}: {response.text}"
        assert response.json()['message'] == 'Ingredient ids must be provided'

        # Удаляем пользователя после теста
        requests.delete(f'{BASE_URL}/api/auth/user', headers=headers)

    def test_create_order_invalid_ingredients(self):
        """Создание заказа с неверным хешем ингредиента."""
        # Создаём пользователя с уникальным email
        email = generate_unique_email()
        data = {
            'email': email,
            'password': 'password123',
            'name': 'OrderUser3'
        }
        response = requests.post(f'{BASE_URL}/api/auth/register', json=data)
        assert response.status_code == 200, f"Registration failed: {response.text}"
        access_token = response.json().get('accessToken')
        assert access_token, "No accessToken in response."
        headers = {'Authorization': access_token}

        order_data = {
            'ingredients': ['invalid_ingredient_id']
        }

        # Пытаемся создать заказ с неверным ингредиентом
        response = requests.post(f'{BASE_URL}/api/orders', headers=headers, json=order_data)
        assert response.status_code == 500, f"Expected 500, got {response.status_code}: {response.text}"

        # Удаляем пользователя после теста
        requests.delete(f'{BASE_URL}/api/auth/user', headers=headers)