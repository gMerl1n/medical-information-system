from django.db import models


class Clinic(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name='Имя клиники')
    legal_address = models.CharField(max_length=1024, unique=True, verbose_name='Юридический адрес')
    physical_address = models.CharField(max_length=1024, unique=True, verbose_name='Физический адрес')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Клиника'
        verbose_name_plural = 'Клиники'
