import pytest
from django.urls import reverse
from django.utils import timezone


@pytest.mark.django_db
def test_get_consultation(auth_client, setup_data):
    client = auth_client(setup_data['doctor_1_user'])
    url = reverse('consultation-detail', args=[setup_data['c1'].id])
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.parametrize(
    'doctor_key, expected_status',
    [
        ('doctor_1', 201),
        ('doctor_2', 400),
    ]
)
def test_create_consultation(auth_client, setup_data, doctor_key, expected_status):
    client = auth_client(setup_data['doctor_1_user'])
    url = reverse('consultation-list')
    payload = {
        'doctor': setup_data[doctor_key].id,
        'patient': setup_data['patient_2'].id,
        'start_time': timezone.now().isoformat(),
        'end_time': timezone.now().isoformat(),
    }
    response = client.post(url, payload, format='json')
    assert response.status_code == expected_status


@pytest.mark.django_db
def test_update_consultation(auth_client, setup_data):
    client = auth_client(setup_data['doctor_1_user'])
    url = reverse('consultation-detail', args=[setup_data['c1'].id])
    payload = {
        'doctor': setup_data['doctor_1'].id,
        'patient': setup_data['patient_1'].id,
        'start_time': timezone.now().isoformat(),
        'end_time': timezone.now().isoformat(),
    }
    response = client.patch(url, payload, format='json')
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_consultation(auth_client, setup_data):
    client = auth_client(setup_data['doctor_1_user'])
    url = reverse('consultation-detail', args=[setup_data['c2'].id])
    response = client.delete(url)
    assert response.status_code == 204


@pytest.mark.django_db
def test_change_status_action(auth_client, setup_data):
    client = auth_client(setup_data['doctor_1_user'])
    url = reverse('consultation-change-status', args=[setup_data['c1'].id])
    status = 'finished'
    payload = {'status': status}
    response = client.post(url, payload, format='json')
    assert response.status_code == 200
    setup_data['c1'].refresh_from_db()
    assert setup_data['c1'].status == status


@pytest.mark.django_db
@pytest.mark.parametrize(
    'user_key, new_status, expected_status_code, should_update',
    [
        ('doctor_1_user', 'finished', 200, True),
        ('patient_1_user', 'finished', 403, False),
    ]
)
def test_change_status_action(auth_client, setup_data, user_key, new_status, expected_status_code, should_update):
    client = auth_client(setup_data[user_key])
    url = reverse('consultation-change-status', args=[setup_data['c1'].id])
    response = client.post(url, {'status': new_status}, format='json')

    assert response.status_code == expected_status_code

    setup_data['c1'].refresh_from_db()
    if should_update:
        assert setup_data['c1'].status == new_status
    else:
        assert setup_data['c1'].status != new_status
