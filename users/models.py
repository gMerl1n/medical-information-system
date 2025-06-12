from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(models.Model):
    ROLE_CHOICES = (
        (1, 'Пациент'),
        (2, 'Доктор'),
        (3, 'Администратор'),
    )

    id = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Роль"
        verbose_name_plural = "Роли"

class User(AbstractUser):
    role_id = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=False, )


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
