from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from rest_framework import renderers

from api.views import CustomUserViewSet, MessageViewSet, ChatViewSet

user_list = CustomUserViewSet.as_view({
    'get': 'list'
})

user_detail = CustomUserViewSet.as_view({
    'get': 'retreive'
})

message_list = MessageViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
message_detail = MessageViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

chat_list = ChatViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
chat_detail = ChatViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})


urlpatterns = [
    path('messages/', message_list, name='message-list'),
    path('messages/<int:pk>/', message_detail, name='message-detail'),
    path('chats/', chat_list, name='chat-list'),
    path('chats/<int:pk>/', chat_detail, name='chat-detail'),
    path('users/', user_list, name='user-list'),
    path('users/<int:pk>/', user_detail, name='user-detail')
]

# router = DefaultRouter()
# router.register(r'users', views.CustomUserViewSet, basename='user')
# router.register(r'messages', views.MessageViewSet, basename='message')
# router.register(r'chats', views.ChatViewSet, basename='chat')

# urlpatterns = [
#     path('', include(router.urls)),
# ]

urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]