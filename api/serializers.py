from rest_framework import serializers
from accounts.models import CustomUser
from api.models import Message, Chat


class CustomUserSerializer(serializers.ModelSerializer):
    created_messages = serializers.SlugRelatedField(
        many=True, 
        read_only=True,
        slug_field="body"
    )

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'chats', 'created_messages']


class MessageSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.username')

    def validate(self, data):
        parent_message = data['parent_message']
        if parent_message is not None and parent_message.chat is not data['chat']:
            raise serializers.ValidationError({
                "parent_message": "parent message must belong to the same chat as the child"
            })
        
        if data['chat'] not in self.context['request'].user.chats.all():
            raise serializers.ValidationError({
                "chat": "message creator is not a member of the chat"
            })

        return data
        
    class Meta:
        model = Message
        fields = ['id', 'chat', 'creator', 'body', 'created', 'parent_message']


class MessageEditSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.username')
    chat = serializers.CharField(read_only=True)
    class Meta:
        model = Message
        fields = ['id', 'chat', 'creator', 'body', 'created', 'parent_message']


    
class ChatSerializer(serializers.ModelSerializer):
    users = serializers.SlugRelatedField(
        many=True, 
        queryset=CustomUser.objects.all(), 
        style={"base_template": "checkbox_multiple.html"}, 
        slug_field="username"
    )

    messages = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    # TODO: can only add friend users
    def validate(self, data):
        if data['type'] == 'personal' and len(data['users']) > 2:
            raise serializers.ValidationError({
                "users": "personal chats are limited to 2 users"
            })
        return data

    class Meta:
        model = Chat
        fields = ['id', 'name', 'created', 'users', 'type', 'messages']
