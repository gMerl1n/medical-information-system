import pytest
from users.models import Patient
from rest_framework.test import APIClient
from django.urls import reverse


@pytest.fixture(scope="function", autouse=True)
def client():
    return APIClient()


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


@pytest.fixture(scope="function")
def consultation_data():
    return {
        "patient": 1,
        "doctor": 3,
        "start_time": "2023-12-31T23:59:59.999999+03:00",
        "end_time": "2024-01-01T00:00:00Z",
    }
