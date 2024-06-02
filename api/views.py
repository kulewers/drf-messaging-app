from accounts.models import CustomUser
from api.models import Message, Chat
from api.serializers import CustomUserSerializer, MessageSerializer, ChatSerializer, MessageEditSerializer
from rest_framework import viewsets
from api.permissions import IsCreatorOrRecipientReadOnly


class CustomUserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsCreatorOrRecipientReadOnly]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.request.method == "PUT":
            serializer_class = MessageEditSerializer

        return serializer_class


class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
