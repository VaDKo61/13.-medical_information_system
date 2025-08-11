import pytest
from django.urls import reverse


@pytest.mark.django_db
@pytest.mark.parametrize(
    'user_key, expected_ids, unexpected_ids',
    [
        ('doctor_1_user', ['c1', 'c2'], ['c3']),
        ('doctor_2_user', ['c3'], ['c1', 'c2']),
        ('patient_1_user', ['c1', 'c3'], ['c2']),
        ('patient_2_user', ['c2'], ['c1', 'c3']),
    ]
)
def test_user_sees_only_their_consultations(auth_client, setup_data, user_key, expected_ids, unexpected_ids):
    client = auth_client(setup_data[user_key])
    url = reverse('consultation-list')
    response = client.get(url)
    assert response.status_code == 200

    ids = {item['id'] for item in response.json()['results']}
    for eid in expected_ids:
        assert setup_data[eid].id in ids
    for uid in unexpected_ids:
        assert setup_data[uid].id not in ids


@pytest.mark.django_db
def test_unauthenticated_user_gets_401(api_client):
    url = reverse('consultation-list')
    response = api_client.get(url)
    assert response.status_code == 401
