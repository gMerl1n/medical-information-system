from .models import Patient
from django.db.models import Q


def _get_user_by_login(username: str, password: str) -> Patient | None:
    patient = Patient.objects.filter(
        Q(username=username) &
        Q(password=password)
    ).first()

    return patient if patient else None