import pytest

from django.urls import reverse

from api.models import Chat, Message
from api.serializers import ChatSerializer, MessageSerializer
from rest_framework import status
from rest_framework.test import APIClient
import json


@pytest.mark.usefixtures("createChats")
@pytest.mark.django_db
def test_list_chats(client, user_A):
    client.force_login(user_A)
    url = reverse('chat-list')
    response = client.get(url)

    chats = Chat.objects.all()
    expected_data = ChatSerializer(chats, many=True).data

    assert response.status_code == status.HTTP_200_OK
    assert response.data['results'] == expected_data

@pytest.mark.django_db
def test_retrieve_chat(client, chat, user_A):
    client.force_login(user_A)
    url = reverse('chat-detail', kwargs={'pk': chat.id})
    response = client.get(url)

    expected_data = ChatSerializer(chat).data

    assert response.status_code == status.HTTP_200_OK
    assert response.data == expected_data


@pytest.mark.usefixtures("createMessages")
@pytest.mark.django_db
def test_list_messages(client, user_admin):
    client.force_login(user_admin)
    url = reverse('message-list')
    response = client.get(url)

    messages = Message.objects.all()
    expected_data = MessageSerializer(messages, many=True).data

    assert response.status_code == status.HTTP_200_OK
    assert response.data['results'] == expected_data

@pytest.mark.django_db
def test_create_message(client, user_A, chat):
    client.force_login(user_A)
    url = reverse('message-list')
    response = client.post(url, {'chat': chat.id, 'body': 'testmessage', 'parent_message': ''})

    message_count = Message.objects.all().count()

    assert response.status_code == status.HTTP_201_CREATED
    assert message_count == 1

@pytest.mark.django_db
def test_retrieve_message(client, message, user_A):
    client.force_login(user_A)
    url = reverse('message-detail', kwargs={'pk': message.id})
    response = client.get(url)

    expected_data = MessageSerializer(message).data

    assert response.status_code == status.HTTP_200_OK
    assert response.data == expected_data

@pytest.mark.django_db
def test_update_message(client, message, user_A):
    client.force_login(user_A)
    url = reverse('message-detail', kwargs={'pk': message.id})

    # drfclient = APIClient()
    # drfclient.force_authenticate(user_A)
    response = client.put(url, json.dumps({'body': 'testupdate'}), content_type='application/json')

    expected_data = MessageSerializer(message).data
    expected_data['body'] = 'testupdate'

    assert response.status_code == status.HTTP_200_OK
    assert response.data == expected_data

@pytest.mark.django_db
def test_destroy_message(client, user_A, message):
    client.force_login(user_A)
    url = reverse('message-detail', kwargs={'pk': message.id})
    response = client.delete(url)

    message_count = Message.objects.all().count()

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert message_count == 0