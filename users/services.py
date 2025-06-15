from .models import Patient, Doctor
from django.db.models import Q


def _get_patient_by_login(username: str, password: str) -> Patient | None:
    patient = Patient.objects.filter(
        Q(username=username) &
        Q(password=password)
    ).first()

    return patient if patient else None


def _get_doctor_by_login(username: str, password: str) -> Doctor | None:
    doctor = Doctor.objects.filter(
        Q(username=username) &
        Q(password=password)
    ).first()

    return doctor if doctor else None
