import requests
import random
import string

BASE_URL = 'https://stellarburgers.nomoreparties.site'


def generate_unique_email():
    """Генерирует случайный уникальный email."""
    return ''.join(random.choices(string.ascii_lowercase, k=10)) + '@example.com'


class TestUserRegistration:

    def test_create_unique_user(self):
        """Создание уникального пользователя."""
        email = generate_unique_email()
        data = {
            'email': email,
            'password': 'password123',
            'name': 'TestUser'
        }
        response = requests.post(f'{BASE_URL}/api/auth/register', json=data)
        assert response.status_code == 200, f"Registration failed: {response.text}"
        assert response.json()['success'] is True

        # Удаляем пользователя после теста
        access_token = response.json().get('accessToken')
        assert access_token, "No accessToken in response."
        headers = {'Authorization': access_token}
        requests.delete(f'{BASE_URL}/api/auth/user', headers=headers)

    def test_create_existing_user(self):
        """Создание пользователя, который уже существует."""
        # Используем уникальный email
        email = generate_unique_email()
        data = {
            'email': email,
            'password': 'password123',
            'name': 'ExistingUser'
        }
        # Регистрируем пользователя первый раз
        response = requests.post(f'{BASE_URL}/api/auth/register', json=data)
        assert response.status_code == 200, f"First registration failed: {response.text}"

        # Пытаемся зарегистрировать его снова
        response = requests.post(f'{BASE_URL}/api/auth/register', json=data)
        assert response.status_code == 403, f"Expected 403, got {response.status_code}: {response.text}"
        assert response.json()['message'] == 'User already exists'

        # Удаляем пользователя после теста
        # Получаем токен через логин
        login_data = {
            'email': email,
            'password': 'password123'
        }
        response = requests.post(f'{BASE_URL}/api/auth/login', json=login_data)
        access_token = response.json().get('accessToken')
        if access_token:
            headers = {'Authorization': access_token}
            requests.delete(f'{BASE_URL}/api/auth/user', headers=headers)

    def test_create_user_missing_field(self):
        """Создание пользователя без обязательного поля."""
        email = generate_unique_email()
        data = {
            'email': email,
            'password': 'password123'
            # Отсутствует поле 'name'
        }
        response = requests.post(f'{BASE_URL}/api/auth/register', json=data)
        assert response.status_code == 403, f"Expected 403, got {response.status_code}: {response.text}"
        assert response.json()['message'] == 'Email, password and name are required fields'