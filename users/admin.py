from django.contrib import admin
from .models import User, Role, Doctor, Patient


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    pass


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    pass


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    pass
