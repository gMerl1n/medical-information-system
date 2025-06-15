from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField
from users.models import Doctor, Patient
from .models import Consultation


class ConsultationSerializer(serializers.ModelSerializer):

    patient = PrimaryKeyRelatedField(queryset=Patient.objects.all())
    doctor = PrimaryKeyRelatedField(queryset=Doctor.objects.all())

    class Meta:
        model = Consultation
        fields = [
            'id',
            'patient',
            'doctor',
            'created_at',
            'start_time',
            'end_time',
            'status'
        ]
        read_only_fields = ['created_at']

    def validate(self, data):
        if data['start_time'] >= data['end_time']:
            raise serializers.ValidationError(
                "Время окончания должно быть позже времени начала."
            )
        return data


class ConsultationChangeStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consultation
        fields = ['status']

    def validate_status(self, value):
        valid_statuses = [choice[0] for choice in Consultation.STATUS_CHOICES]
        if value not in valid_statuses:
            raise serializers.ValidationError(
                f"Status {valid_statuses} is invalid"
            )
        return value