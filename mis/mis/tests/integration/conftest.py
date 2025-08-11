from datetime import timedelta

import pytest

from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from app.models import Doctor, Consultation, Patient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_user(django_user_model):
    def _make_user(**kwargs):
        return django_user_model.objects.create_user(**kwargs)

    return _make_user


@pytest.fixture
def auth_client(api_client):
    def _make_authenticated(user):
        refresh = RefreshToken.for_user(user)
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        return api_client

    return _make_authenticated


@pytest.fixture
def setup_data(create_user):
    users_info = [
        ('adm', 'admin', Doctor, '', '', ''),
        ('doctor_1', 'doctor', Doctor, 'Иван', 'Иванов', 'Иванович'),
        ('doctor_2', 'doctor', Doctor, 'Петр', 'Петров', 'Петрович'),
        ('patient_1', 'patient', Patient, 'Анна', 'Быстрая', 'Геннадьевна'),
        ('patient_2', 'patient', Patient, 'Мария', 'Сидорова', 'Сидоровна'),
    ]

    users = {}
    profiles = {}

    for username, role, model_cls, first, last, sur in users_info:
        user = create_user(username=username, password='pass', role=role)
        users[f'{username}_user'] = user
        profiles[username] = model_cls.objects.create(
            first_name=first,
            last_name=last,
            surname=sur,
            user=user
        )

    now = timezone.now()
    earlier = now - timedelta(days=2)
    later = now + timedelta(days=1)

    consultations_info = [
        ('doctor_1', 'patient_1', 'confirmed', earlier),
        ('doctor_1', 'patient_2', 'pending', later),
        ('doctor_2', 'patient_1', 'paid', now),
    ]

    consultations = {}
    for i, (doc_key, pat_key, status, created_at) in enumerate(consultations_info, start=1):
        consultations[f'c{i}'] = Consultation.objects.create(
            start_time=now,
            end_time=now,
            doctor=profiles[doc_key],
            patient=profiles[pat_key],
            status=status,
            created_at=created_at
        )

    return {
        **users,
        'adm': profiles['adm'],
        'doctor_1': profiles['doctor_1'],
        'doctor_2': profiles['doctor_2'],
        'patient_1': profiles['patient_1'],
        'patient_2': profiles['patient_2'],
        **consultations,
    }
