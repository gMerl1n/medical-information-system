from rest_framework import serializers
from .models import Role, Doctor, Patient


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id']


class PatientSerializer(serializers.ModelSerializer):
    role_id = RoleSerializer(many=True, read_only=True)

    class Meta:
        model = Patient
        fields = ['id', 'first_name', 'role_id', 'last_name', 'patronymic', 'username', 'password', 'email']


class DoctorSerializer(serializers.ModelSerializer):
    role_id = RoleSerializer(many=True, read_only=True)

    class Meta:
        model = Doctor
        fields = ['id', 'first_name', 'last_name', 'patronymic', 'speciality', 'created_at', 'updated_at']


