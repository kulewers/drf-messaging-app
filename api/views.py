from accounts.models import CustomUser
from api.models import Message, Chat
from api.serializers import CustomUserSerializer, MessageSerializer, ChatSerializer
from rest_framework import viewsets
from api.permissions import IsCreatorOrRecipientReadOnly, IsCreator, IsCreatorOrAdminUser
from rest_framework.permissions import IsAuthenticated, IsAdminUser


class CustomUserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
    
    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAdminUser]
        elif self.action == 'destroy':
            permission_classes = [IsCreatorOrAdminUser]
        else:
            permission_classes = [IsAuthenticated, IsCreatorOrRecipientReadOnly]
        return [permission() for permission in permission_classes]
    

class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]
