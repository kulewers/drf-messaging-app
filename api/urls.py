from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api import views

router = DefaultRouter()
router.register(r'users', views.CustomUserViewSet, basename='user')
router.register(r'messages', views.MessageViewSet, basename='message')
router.register(r'chats', views.ChatViewSet, basename='chat')

urlpatterns = [
    path('', include(router.urls)),
]

urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]