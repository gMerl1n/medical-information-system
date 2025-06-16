from rest_framework import serializers
from clinics.models import Clinic
from .models import Doctor, Patient, Admin


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ('id', 'first_name', 'role', 'phone', 'last_name', 'patronymic', 'username', 'password', 'email')


class DoctorSerializer(serializers.ModelSerializer):
    clinic = serializers.PrimaryKeyRelatedField(queryset=Clinic.objects.all())

    def create(self, validated_data):
        clinic = Clinic.objects.filter(name=validated_data["clinic"]).first()
        validated_data.pop("clinic")
        doctor = Doctor.objects.create(**validated_data)
        clinic.doctor_set.add(doctor)

        doctor.save()

        return doctor

    class Meta:
        model = Doctor
        fields = (
            'id',
            'username',
            'first_name',
            'role',
            'clinic',
            'last_name',
            'patronymic',
            'speciality',
            'created_at',
            'updated_at'
        )


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ('id', 'first_name', 'role', 'last_name', 'username', 'password', 'email')
