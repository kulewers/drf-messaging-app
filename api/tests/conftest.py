import pytest
from ..models import Chat, Message
from accounts.models import CustomUser

@pytest.fixture
def user_A(db):
    return CustomUser.objects.create_user('testuser1', 'test1@test.com', 'testpassword')

@pytest.fixture
def user_admin(db):
    return CustomUser.objects.create_user('testuseradmin', 'testadmin@test.com', 'testpassword', is_staff=True)

@pytest.fixture
def user_B(db):
    return CustomUser.objects.create_user('testuser2', 'test2@test.com', 'testpassword')

@pytest.fixture
def chat(db, user_A, user_B):
    chat = Chat.objects.create(name='testchat', type='group')
    chat.users.set([user_A, user_B])
    return chat

@pytest.fixture
def message(db, user_A, chat):
    return Message.objects.create(chat=chat, creator=user_A, body='testmessage')

@pytest.fixture()
def createChats(db, user_A, user_B):
    chat1 = Chat.objects.create(name='testchat1', type='group')
    chat1.users.set([user_A, user_B])
    chat2 = Chat.objects.create(name='testchat2', type='group')
    chat2.users.set([user_A, user_B])

@pytest.fixture()
def createMessages(db, user_A, user_B, chat):
    Message.objects.create(chat=chat, creator=user_A, body='testmessage1')
    Message.objects.create(chat=chat, creator=user_B, body='testmessage2')
