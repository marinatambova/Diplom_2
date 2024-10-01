import requests
import random
import string

BASE_URL = 'https://stellarburgers.nomoreparties.site'


def generate_unique_email():
    """Генерирует случайный уникальный email."""
    return ''.join(random.choices(string.ascii_lowercase, k=10)) + '@example.com'


class TestUserLogin:

    def test_login_existing_user(self):
        """Логин под существующим пользователем."""
        # Создаём пользователя с уникальным email
        email = generate_unique_email()
        data = {
            'email': email,
            'password': 'password123',
            'name': 'LoginUser'
        }
        # Регистрируем пользователя
        response = requests.post(f'{BASE_URL}/api/auth/register', json=data)
        assert response.status_code == 200, f"Registration failed: {response.text}"

        # Пытаемся войти
        login_data = {
            'email': email,
            'password': 'password123'
        }
        response = requests.post(f'{BASE_URL}/api/auth/login', json=login_data)
        assert response.status_code == 200, f"Login failed: {response.text}"
        assert response.json()['success'] is True

        # Удаляем пользователя после теста
        access_token = response.json().get('accessToken')
        assert access_token, "No accessToken in login response."
        headers = {'Authorization': access_token}
        requests.delete(f'{BASE_URL}/api/auth/user', headers=headers)

    def test_login_incorrect_password(self):
        """Логин с неверным паролем."""
        # Создаём пользователя с уникальным email
        email = generate_unique_email()
        data = {
            'email': email,
            'password': 'password123',
            'name': 'LoginUser2'
        }
        # Регистрируем пользователя
        response = requests.post(f'{BASE_URL}/api/auth/register', json=data)
        assert response.status_code == 200, f"Registration failed: {response.text}"

        # Пытаемся войти с неверным паролем
        login_data = {
            'email': email,
            'password': 'wrongpassword'
        }
        response = requests.post(f'{BASE_URL}/api/auth/login', json=login_data)
        assert response.status_code == 401, f"Expected 401, got {response.status_code}: {response.text}"
        assert response.json()['message'] == 'email or password are incorrect'

        # Удаляем пользователя после теста
        # Нужно войти с правильным паролем, чтобы получить токен для удаления
        login_data = {
            'email': email,
            'password': 'password123'
        }
        response = requests.post(f'{BASE_URL}/api/auth/login', json=login_data)
        access_token = response.json().get('accessToken')
        assert access_token, "No accessToken in login response."
        headers = {'Authorization': access_token}
        requests.delete(f'{BASE_URL}/api/auth/user', headers=headers)