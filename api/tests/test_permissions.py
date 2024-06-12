from rest_framework import status
from django.urls import reverse
import json

import pytest


@pytest.mark.django_db
def test_list_message_restricted_to_staff(client, user_A, user_admin):
    url = reverse('message-list')

    response_unauthorized = client.get(url)
    client.force_login(user=user_A)
    response_authorized_not_staff = client.get(url)
    client.force_login(user=user_admin)
    response_authorized_staff = client.get(url)

    assert response_unauthorized.status_code == status.HTTP_401_UNAUTHORIZED
    assert response_authorized_not_staff.status_code == status.HTTP_403_FORBIDDEN
    assert response_authorized_staff.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_create_message_restricted_to_authorized_user(client, chat, user_A):
    url = reverse('message-list')
    data = {'chat': chat.id, 'body': 'testmesage', 'parent_message': ''}

    response_unauthorized = client.post(url, json.dumps(data), content_type='application/json')
    client.force_login(user=user_A)
    response_authorized = client.post(url, json.dumps(data), content_type='application/json')

    assert response_unauthorized.status_code == status.HTTP_401_UNAUTHORIZED
    assert response_authorized.status_code == status.HTTP_201_CREATED

@pytest.mark.django_db
def test_retrieve_message_restricted_to_creator_or_recipient(client, user_A, user_B, message):
    url = reverse('message-detail', kwargs={'pk': message.id})

    response_unauthorized = client.get(url)
    client.force_login(user=user_A)
    response_authorized_creator = client.get(url)
    client.force_login(user=user_B)
    response_authorized_recipient = client.get(url)

    assert response_unauthorized.status_code == status.HTTP_401_UNAUTHORIZED
    assert response_authorized_creator.status_code == status.HTTP_200_OK
    assert response_authorized_recipient.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_destroy_message_restricted_to_creator(client, user_A, user_B, message):
    url = reverse('message-detail', kwargs={'pk': message.id})

    response_unauthorized = client.delete(url)
    client.force_login(user=user_B)
    response_authorized_recipient = client.delete(url)
    client.force_login(user=user_A)
    response_authorized_creator = client.delete(url)

    assert response_unauthorized.status_code == status.HTTP_401_UNAUTHORIZED
    assert response_authorized_recipient.status_code == status.HTTP_403_FORBIDDEN
    assert response_authorized_creator.status_code == status.HTTP_204_NO_CONTENT