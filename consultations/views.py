from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .filters import ConsultationFilter
from .serializers import ConsultationSerializer, ConsultationChangeStatusSerializer
from .models import Consultation
from users.permissions import IsAdmin, IsDoctor, IsPatient


class CreateConsultation(generics.CreateAPIView):
    queryset = Consultation.objects.all()
    serializer_class = ConsultationSerializer
    permission_classes = [IsPatient]


class ListConsultations(generics.ListAPIView):
    queryset = Consultation.objects.all()
    serializer_class = ConsultationSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ConsultationFilter

    permission_classes = [IsAdmin | IsDoctor | IsPatient]


class ConsultationDetail(generics.RetrieveAPIView):
    queryset = Consultation.objects.all()
    serializer_class = ConsultationSerializer
    permission_classes = [IsAdmin | IsDoctor | IsPatient]


class RemoveConsultation(generics.DestroyAPIView):
    queryset = Consultation.objects.all()
    serializer_class = ConsultationSerializer
    permission_classes = [IsAdmin | IsDoctor | IsPatient]


class ConsultationUpdate(generics.UpdateAPIView):
    queryset = Consultation.objects.all()
    serializer_class = ConsultationChangeStatusSerializer
    http_method_names = ['patch']
    permission_classes = [IsDoctor]
