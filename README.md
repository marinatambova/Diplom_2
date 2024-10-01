# Diplom_2

## Описание проекта

**Diplom_2** — это проект для задания 2 дипломной работы по курсу "Тестирование". Здесь реализованы автотесты для API сервиса **Stellar Burgers**.

Тесты покрывают следующие эндпоинты API:

- Создание пользователя
- Логин пользователя
- Изменение данных пользователя
- Создание заказа
- Получение заказов конкретного пользователя

## Структура проекта
Diplom_2/
├── .gitignore
├── README.md
├── requirements.txt
├── conftest.py
├── tests/
│ ├── init.py
│ ├── test_user_registration.py
│ ├── test_user_login.py
│ ├── test_user_data_change.py
│ ├── test_order_creation.py
│ └── test_get_user_orders.py


- **`.gitignore`** — файл с перечислением файлов и папок, игнорируемых Git.
- **`README.md`** — данный файл с описанием проекта.
- **`requirements.txt`** — файл с зависимостями проекта.
- **`conftest.py`** — файл с общими фикстурами для тестов.
- **`tests/`** — директория с тестовыми файлами.
