import requests
import random
import string

BASE_URL = 'https://stellarburgers.nomoreparties.site'


def generate_unique_email():
    """Генерирует случайный уникальный email."""
    return ''.join(random.choices(string.ascii_lowercase, k=10)) + '@example.com'


class TestGetUserOrders:

    def test_get_orders_authorized(self):
        """Получение заказов авторизованным пользователем."""
        # Создаём пользователя с уникальным email
        email = generate_unique_email()
        data = {
            'email': email,
            'password': 'password123',
            'name': 'OrdersUser'
        }
        # Регистрируем пользователя
        response = requests.post(f'{BASE_URL}/api/auth/register', json=data)
        assert response.status_code == 200, f"Registration failed: {response.text}"
        access_token = response.json().get('accessToken')
        assert access_token, "No accessToken in response."
        headers = {'Authorization': access_token}

        # Получаем заказы пользователя
        response = requests.get(f'{BASE_URL}/api/orders', headers=headers)
        assert response.status_code == 200, f"Failed to get orders: {response.text}"
        assert response.json()['success'] is True

        # Удаляем пользователя после теста
        requests.delete(f'{BASE_URL}/api/auth/user', headers=headers)

    def test_get_orders_unauthorized(self):
        """Получение заказов без авторизации."""
        # Пытаемся получить заказы без токена
        response = requests.get(f'{BASE_URL}/api/orders')
        assert response.status_code == 401, f"Expected 401, got {response.status_code}: {response.text}"
        assert response.json()['message'] == 'You should be authorised'