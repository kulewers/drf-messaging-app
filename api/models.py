from django.db import models


class Chat(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    type = models.CharField(choices=[('personal','Personal'), ('group','Group')], default='personal', max_length=100)
    users = models.ManyToManyField('accounts.CustomUser', through='ChatParticipants', related_name='chats')

    def __str__(self):
        return self.name
    

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    creator = models.ForeignKey('accounts.CustomUser', related_name='created_messages', on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    parent_message = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.body


class ChatParticipants(models.Model):
    user = models.ForeignKey("accounts.CustomUser", on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
