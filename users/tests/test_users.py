import pytest
from django.urls import reverse
from users.models import Patient, Doctor
from clinics.models import Clinic


class TestUser:

    @pytest.mark.django_db(transaction=True)
    def create_clinic(self):
        clinic = Clinic.objects.create(
            name="Clinic",
            legal_address="Legal Address",
            physical_address="Physical Address"
        )

        clinic.save()

        return clinic

    @pytest.mark.django_db(transaction=True)
    def create_doctor(self) -> Doctor:
        doctor_data = {
            "username": "user_doctor",
            "password": "password_doctor",
            "first_name": "first_name_doctor",
            "last_name": "last_name_doctor",
            "patronymic": "patronymic_doctor",
            "email": "emai_doctor@email.ru",
            "speciality": "specialty_doctor",
            "role": 2
        }

        doctor = Doctor.objects.create(**doctor_data)

        clinic = self.create_clinic()

        clinic.doctor_set.add(doctor)

        doctor.save()

        return doctor

    @pytest.mark.django_db(transaction=True)
    def create_patient(self) -> Patient:
        patient_data = {
            "username": "user_patient",
            "password": "password_patient",
            "first_name": "first_name_patient",
            "last_name": "last_name_patient",
            "patronymic": "patronymic_patient",
            "email": "email_patient@email.ru",
            "phone": "phone_patient",
            "role": 1
        }

        patient = Patient.objects.create(**patient_data)

        patient.save()

        return patient

    @pytest.mark.django_db(transaction=True)
    def test_register_patient_already_exists_in_db(self, client, patient_data):
        self.create_patient()

        response = client.post(reverse("register_patient"), data=patient_data)
        assert response.status_code == 500

    @pytest.mark.django_db(transaction=True)
    def test_register_patient(self, client, patient_data):
        response = client.post(reverse("register_patient"), data=patient_data)
        assert response.status_code == 201
        assert Patient.objects.filter(username='user_patient').exists()

    @pytest.mark.django_db(transaction=True)
    def test_register_doctor(self, client, doctor_data):
        clinic = self.create_clinic()

        doctor_data.update({
            "clinic": clinic.id
        })

        response = client.post(reverse("register_doctor"), data=doctor_data)
        assert response.status_code == 201
        assert Doctor.objects.filter(username='user_doctor').exists()

    @pytest.mark.django_db(transaction=True)
    def test_login_patient(self, client, login_patient_data):
        self.create_patient()

        response = client.post(reverse("login_patient"), data=login_patient_data)
        access_token = response.data.get("access")
        assert response.status_code == 200
        assert access_token is not None

    @pytest.mark.django_db(transaction=True)
    def test_login_doctor(self, client, login_doctor_data):
        self.create_doctor()

        response = client.post(reverse("login_doctor"), data=login_doctor_data)
        access_token = response.data.get("access")
        assert response.status_code == 200
        assert access_token is not None
