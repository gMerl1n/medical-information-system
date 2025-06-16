from rest_framework import permissions
from mis.settings import PATIENT_ROLE, DOCTOR_ROLE, ADMIN_ROLE


class IsDoctor(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == DOCTOR_ROLE)


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == ADMIN_ROLE)


class IsPatient(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == PATIENT_ROLE)
