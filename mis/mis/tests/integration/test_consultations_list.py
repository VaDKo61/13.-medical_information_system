import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_list_consultations_sorted_by_created_at(auth_client, setup_data):
    client = auth_client(setup_data['doctor_1_user'])
    url = reverse('consultation-list') + '?ordering=created_at'
    response = client.get(url)
    assert response.status_code == 200
    dates = [item['created_at'] for item in response.json()['results']]
    assert dates == sorted(dates)


@pytest.mark.django_db
@pytest.mark.parametrize(
    'param, value, field',
    [
        ('doctor_name', 'Иван', 'doctor.first_name'),
        ('patient_name', 'Анна', 'patient.first_name'),
    ]
)
def test_list_consultations_search_by_admin(auth_client, setup_data, param, value, field):
    client = auth_client(setup_data['adm_user'])
    url = reverse('consultation-list') + f'?{param}={value}'
    response = client.get(url)
    assert response.status_code == 200
    for item in response.json()['results']:
        key1, key2 = field.split('.')
        assert value in item[key1][key2]


@pytest.mark.django_db
def test_list_consultations_filter_by_status(auth_client, setup_data):
    client = auth_client(setup_data['adm_user'])
    status = 'paid'
    url = reverse('consultation-list') + f'?status={status}'
    response = client.get(url)
    assert response.status_code == 200
    for item in response.json()['results']:
        assert item['status'] == status
