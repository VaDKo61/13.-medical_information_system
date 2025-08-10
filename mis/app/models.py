from django.db import models

from user.models import User


class Clinic(models.Model):
    name = models.CharField(max_length=200)
    legal_address = models.CharField(max_length=300)
    physical_address = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class Doctor(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    surname = models.CharField(max_length=150)
    specialization = models.CharField(max_length=200)
    clinics = models.ManyToManyField(Clinic, related_name='doctors')
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')

    def __str__(self):
        return f'{self.last_name} {self.first_name}'


class Patient(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    surname = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_profile')

    def __str__(self):
        return f'{self.last_name} {self.first_name}'


class Consultation(models.Model):
    STATUS_CHOICES = [
        ('confirmed', 'подтверждена'),
        ('pending', 'ожидает'),
        ('started', 'начата'),
        ('finished', 'завершена'),
        ('paid', 'оплачена'),
    ]
    created_at = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='confirmed')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='consultations')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='consultations')

    def __str__(self):
        return f'Консультация {self.start_time}, {self.patient} с доктором {self.doctor}'
