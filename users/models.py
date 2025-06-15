from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        (1, "Patient"),
        (2, "Doctor"),
        (3, "Admin"),
    )
    role = models.IntegerField(choices=ROLE_CHOICES, null=True, blank=False)


class Patient(User):
    patronymic = models.CharField(max_length=255, blank=False)
    phone = models.CharField(max_length=255, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Пациент"
        verbose_name_plural = "Пациенты"


class Doctor(User):
    patronymic = models.CharField(max_length=255, blank=False, verbose_name='Отчество')
    speciality = models.CharField(max_length=255, blank=False, verbose_name='Специализация')
    clinic = models.ManyToManyField("clinics.Clinic")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Врач"
        verbose_name_plural = "Врачи"
