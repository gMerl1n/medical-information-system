from django.db import models

class Consultation(models.Model):
    STATUS_CHOICES = (
            ('confirmed', 'Подтверждена'),
            ('pending', 'Ожидает'),
            ('started', 'Начата'),
            ('completed', 'Завершена'),
            ('paid', 'Оплачена'),
    )
    patient = models.ForeignKey("users.Patient", related_name="consultations_patient", on_delete=models.CASCADE)
    doctor = models.ForeignKey("users.Doctor", related_name="consultations_doctor", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    start_time = models.DateTimeField(verbose_name='Время начала')
    end_time = models.DateTimeField(verbose_name='Время окончания')
    status = models.CharField(
        max_length=255,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Статус'
    )

    class Meta:
        verbose_name = 'Консультация'
        verbose_name_plural = 'Консультации'
