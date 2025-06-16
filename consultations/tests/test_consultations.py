import pytest
from users.models import Doctor, Patient, Admin
from mis.settings import PATIENT_ROLE, DOCTOR_ROLE, ADMIN_ROLE
from consultations.models import Consultation
from clinics.models import Clinic
from django.urls import reverse


class TestConsultation:

    @pytest.mark.django_db
    def create_clinic(self):
        clinic = Clinic.objects.create(
            name="Clinic",
            legal_address="Legal Address",
            physical_address="Physical Address"
        )

        clinic.save()

        return clinic

    @pytest.mark.django_db
    def create_doctor(self) -> Doctor:
        doctor_data = {
            "username": "user_doctor",
            "password": "password_doctor",
            "first_name": "first_name_doctor",
            "last_name": "last_name_doctor",
            "patronymic": "patronymic_doctor",
            "email": "emai_doctor@email.ru",
            "speciality": "specialty_doctor",
            "role": DOCTOR_ROLE
        }

        doctor = Doctor.objects.create(**doctor_data)

        clinic = self.create_clinic()

        clinic.doctor_set.add(doctor)

        doctor.save()

        return doctor

    @pytest.mark.django_db
    def create_patient(self) -> Patient:
        patient_data = {
            "username": "user_patient",
            "password": "password_patient",
            "first_name": "first_name_patient",
            "last_name": "last_name_patient",
            "patronymic": "patronymic_patient",
            "email": "email_patient@email.ru",
            "phone": "phone_patient",
            "role": PATIENT_ROLE
        }

        patient = Patient.objects.create(**patient_data)

        patient.save()

        return patient

    @pytest.mark.django_db
    def create_consultation(self, patient: Patient, doctor: Doctor) -> Consultation:
        consultation = {
            "start_time": "2023-12-31T23:59:59.999999+03:00",
            "end_time": "2024-01-01T00:00:00Z",
            "patient": patient,
            "doctor": doctor,
        }

        consultation = Consultation.objects.create(**consultation)

        consultation.save()

        return consultation

    @pytest.mark.django_db(transaction=True)
    def create_admin(self) -> Admin:
        admin_data = {
            "username": "user_admin",
            "password": "password_admin",
            "first_name": "first_name_admin",
            "last_name": "last_name_admin",
            "email": "email_admin@email.ru",
            "role": ADMIN_ROLE
        }

        admin = Admin.objects.create(**admin_data)

        admin.save()

        return admin

    @pytest.mark.django_db
    def test_create_consultation_by_non_auth_user(self,
                                                  client,
                                                  consultation_data):
        doctor = self.create_doctor()
        patient = self.create_patient()

        consultation_data.update(
            {
                "patient": patient.id,
                "doctor": doctor.id,
            }
        )

        response = client.post(reverse("create_consultation"), data=consultation_data)
        assert response.status_code == 401

    @pytest.mark.django_db
    def test_get_list_consultations_by_non_auth_user(self,
                                                     client,
                                                     consultation_data):
        doctor = self.create_doctor()
        patient = self.create_patient()
        self.create_consultation(patient, doctor)

        response = client.get(reverse("list_consultation"), data=consultation_data)
        assert response.status_code == 401

    @pytest.mark.django_db
    def test_get_consultations_by_id_by_non_auth_user(self,
                                                      client,
                                                      login_patient_data,
                                                      consultation_data):
        doctor = self.create_doctor()
        patient = self.create_patient()
        consultation = self.create_consultation(patient, doctor)

        response = client.get(reverse("consultation_detail", args=[consultation.id]))

        assert response.status_code == 401

    @pytest.mark.django_db
    def test_remove_consultations_by_id_by_non_auth_user(self,
                                                         client,
                                                         login_patient_data,
                                                         consultation_data):
        doctor = self.create_doctor()
        patient = self.create_patient()
        consultation = self.create_consultation(patient, doctor)

        response = client.delete(reverse("remove_consultation", args=[consultation.id]))
        assert response.status_code == 401

    @pytest.mark.django_db
    def test_update_consultations_by_id_by_non_auth_user(self,
                                                         client,
                                                         login_doctor_data,
                                                         consultation_data):
        doctor = self.create_doctor()
        patient = self.create_patient()
        consultation = self.create_consultation(patient, doctor)

        data = {
            "status": "completed"
        }

        response = client.patch(reverse("consultation_update", args=[consultation.id]), data=data)
        assert response.status_code == 401

    @pytest.mark.django_db
    def test_create_consultation_by_admin(self,
                                          client,
                                          login_admin_data,
                                          consultation_data):
        doctor = self.create_doctor()
        patient = self.create_patient()
        self.create_admin()

        consultation_data.update(
            {
                "patient": patient.id,
                "doctor": doctor.id,
            }
        )

        response = client.post(reverse("login_admin"), data=login_admin_data)
        access_token = response.data.get("access")
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        response = client.post(reverse("create_consultation"), data=consultation_data)
        assert response.status_code == 403

    @pytest.mark.django_db
    def test_create_consultation_by_patient(self,
                                            client,
                                            patient_data,
                                            login_patient_data,
                                            consultation_data):
        doctor = self.create_doctor()
        patient = self.create_patient()

        consultation_data.update(
            {
                "patient": patient.id,
                "doctor": doctor.id,
            }
        )

        response = client.post(reverse("login_patient"), data=login_patient_data, format='json')
        access_token = response.data.get("access")
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        response = client.post(reverse("create_consultation"), data=consultation_data)
        assert response.status_code == 201

    @pytest.mark.django_db
    def test_get_list_consultations_by_admin(self,
                                             client,
                                             login_admin_data,
                                             consultation_data):
        doctor = self.create_doctor()
        patient = self.create_patient()
        self.create_admin()
        self.create_consultation(patient, doctor)

        response = client.post(reverse("login_admin"), data=login_admin_data)
        access_token = response.data.get("access")
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        response = client.get(reverse("list_consultation"), data=consultation_data)
        assert response.status_code == 200
        assert len(response.data) == 1

    @pytest.mark.django_db
    def test_get_list_consultations_by_patient(self,
                                               client,
                                               login_patient_data,
                                               consultation_data):
        doctor = self.create_doctor()
        patient = self.create_patient()
        self.create_consultation(patient, doctor)

        response = client.post(reverse("login_patient"), data=login_patient_data, format='json')
        access_token = response.data.get("access")
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        response = client.get(reverse("list_consultation"), data=consultation_data)
        assert response.status_code == 200
        assert len(response.data) == 1

    @pytest.mark.django_db
    def test_get_list_consultations_by_doctor(self,
                                              client,
                                              login_doctor_data,
                                              consultation_data):
        doctor = self.create_doctor()
        patient = self.create_patient()
        self.create_consultation(patient, doctor)

        response = client.post(reverse("login_doctor"), data=login_doctor_data, format='json')

        access_token = response.data.get("access")
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        response = client.get(reverse("list_consultation"), data=consultation_data)
        assert response.status_code == 200
        assert len(response.data) == 1

    @pytest.mark.django_db
    def test_get_consultation_by_id_by_admin(self,
                                               client,
                                               login_admin_data,
                                               consultation_data):
        doctor = self.create_doctor()
        patient = self.create_patient()
        self.create_admin()
        consultation = self.create_consultation(patient, doctor)

        response = client.post(reverse("login_admin"), data=login_admin_data)
        access_token = response.data.get("access")
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        response = client.get(reverse("consultation_detail", args=[consultation.id]))

        consultation_response = response.data
        assert response.status_code == 200
        assert consultation_response["status"] == "pending"

    @pytest.mark.django_db
    def test_get_consultation_by_id_by_patient(self,
                                                client,
                                                login_patient_data,
                                                consultation_data):
        doctor = self.create_doctor()
        patient = self.create_patient()
        consultation = self.create_consultation(patient, doctor)

        response = client.post(reverse("login_patient"), data=login_patient_data)
        access_token = response.data.get("access")
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        response = client.get(reverse("consultation_detail", args=[consultation.id]))

        consultation_response = response.data
        assert response.status_code == 200
        assert consultation_response["status"] == "pending"

    @pytest.mark.django_db
    def test_get_consultation_by_id_by_doctor(self,
                                               client,
                                               login_doctor_data,
                                               consultation_data):
        doctor = self.create_doctor()
        patient = self.create_patient()
        consultation = self.create_consultation(patient, doctor)

        response = client.post(reverse("login_doctor"), data=login_doctor_data)
        access_token = response.data.get("access")
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        response = client.get(reverse("consultation_detail", args=[consultation.id]))

        consultation_response = response.data
        assert response.status_code == 200
        assert consultation_response["status"] == "pending"

    @pytest.mark.django_db
    def test_update_consultations_by_id_by_patient(self,
                                                   client,
                                                   login_patient_data,
                                                   consultation_data):
        doctor = self.create_doctor()
        patient = self.create_patient()
        consultation = self.create_consultation(patient, doctor)

        response = client.patch(reverse("login_patient"), data=login_patient_data)
        access_token = response.data.get("access")
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        data = {
            "status": "completed"
        }

        response = client.patch(reverse("consultation_update", args=[consultation.id]), data=data)
        assert response.status_code == 401

    @pytest.mark.django_db
    def test_update_consultations_by_id_by_doctor(self,
                                                  client,
                                                  login_doctor_data,
                                                  consultation_data):
        doctor = self.create_doctor()
        patient = self.create_patient()
        consultation = self.create_consultation(patient, doctor)

        response = client.post(reverse("login_doctor"), data=login_doctor_data)

        access_token = response.data.get("access")
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        data = {
            "status": "completed"
        }

        response = client.patch(reverse("consultation_update", args=[consultation.id]), data=data)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_remove_consultations_by_id_by_patient(self,
                                                   client,
                                                   login_admin_data,
                                                   consultation_data):
        doctor = self.create_doctor()
        patient = self.create_patient()
        self.create_admin()
        consultation = self.create_consultation(patient, doctor)

        response = client.post(reverse("login_admin"), data=login_admin_data)
        access_token = response.data.get("access")

        client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        response = client.delete(reverse("remove_consultation", args=[consultation.id]))
        assert response.status_code == 204

    @pytest.mark.django_db
    def test_remove_consultations_by_id_by_patient(self,
                                                   client,
                                                   login_patient_data,
                                                   consultation_data):
        doctor = self.create_doctor()
        patient = self.create_patient()
        consultation = self.create_consultation(patient, doctor)

        response = client.post(reverse("login_patient"), data=login_patient_data)
        access_token = response.data.get("access")

        client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        response = client.delete(reverse("remove_consultation", args=[consultation.id]))
        assert response.status_code == 204

    @pytest.mark.django_db
    def test_remove_consultations_by_id_by_doctor(self,
                                                  client,
                                                  login_doctor_data,
                                                  consultation_data):
        doctor = self.create_doctor()
        patient = self.create_patient()
        consultation = self.create_consultation(patient, doctor)

        response = client.post(reverse("login_doctor"), data=login_doctor_data)
        access_token = response.data.get("access")
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        response = client.delete(reverse("remove_consultation", args=[consultation.id]))
        assert response.status_code == 204
