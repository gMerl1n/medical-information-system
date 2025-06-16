import pytest
from rest_framework.test import APIClient


@pytest.fixture(scope="function", autouse=True)
def client():
    return APIClient()


@pytest.fixture(scope="function")
def admin_data():
    return {
        "username": "user_admin",
        "password": "password_admin",
        "first_name": "first_name_admin",
        "last_name": "last_name_admin",
        "email": "email_admin@email.ru",
        "role": 3
    }


@pytest.fixture(scope="function")
def login_admin_data():
    return {
        "username": "user_admin",
        "password": "password_admin",
    }


@pytest.fixture(scope="function")
def patient_data():
    return {
        "username": "user_patient",
        "password": "password_patient",
        "first_name": "first_name_patient",
        "last_name": "last_name_patient",
        "patronymic": "patronymic_patient",
        "email": "email_patient@email.ru",
        "phone": "phone_patient",
        "role": 1
    }


@pytest.fixture(scope="function")
def login_patient_data():
    return {
        "username": "user_patient",
        "password": "password_patient",
    }


@pytest.fixture(scope="function")
def doctor_data():
    return {
        "username": "user_doctor",
        "password": "password_doctor",
        "first_name": "first_name_doctor",
        "last_name": "last_name_doctor",
        "patronymic": "patronymic_doctor",
        "clinic": 1,
        "email": "emai_doctor@email.ru",
        "speciality": "specialty_doctor",
        "role": 2
    }


@pytest.fixture(scope="function")
def login_doctor_data():
    return {
        "username": "user_doctor",
        "password": "password_doctor",
    }
