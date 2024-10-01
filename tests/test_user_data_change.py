import requests
import random
import string

BASE_URL = 'https://stellarburgers.nomoreparties.site'


def generate_unique_email():
    """Генерирует случайный уникальный email."""
    return ''.join(random.choices(string.ascii_lowercase, k=10)) + '@example.com'


class TestUserDataChange:

    def test_change_user_data_authorized(self):
        """Изменение данных пользователя с авторизацией."""
        # Создаём пользователя с уникальным email
        email = generate_unique_email()
        data = {
            'email': email,
            'password': 'password123',
            'name': 'ChangeUser'
        }
        response = requests.post(f'{BASE_URL}/api/auth/register', json=data)
        assert response.status_code == 200, f"Registration failed: {response.text}"
        access_token = response.json().get('accessToken')
        assert access_token is not None, "No accessToken in response."
        headers = {'Authorization': access_token}

        # Генерируем новый уникальный email для изменения данных
        new_email = generate_unique_email()
        new_data = {
            'email': new_email,
            'name': 'NewName'
        }
        response = requests.patch(f'{BASE_URL}/api/auth/user', headers=headers, json=new_data)
        assert response.status_code == 200, f"Data change failed: {response.text}"
        assert response.json()['user']['email'] == new_email
        assert response.json()['user']['name'] == 'NewName'

        # Удаляем пользователя после теста
        requests.delete(f'{BASE_URL}/api/auth/user', headers=headers)

    def test_change_user_data_unauthorized(self):
        """Изменение данных пользователя без авторизации."""
        # Пытаемся изменить данные без токена
        new_data = {
            'email': 'unauthuser@example.com',
            'name': 'UnauthName'
        }
        response = requests.patch(f'{BASE_URL}/api/auth/user', json=new_data)
        assert response.status_code == 401, f"Expected 401, got {response.status_code}: {response.text}"
        assert response.json()['message'] == 'You should be authorised'