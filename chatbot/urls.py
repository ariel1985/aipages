from django.urls import path
from . import views

app_name = 'chatbot'

urlpatterns = [
    path('', views.chat_view, name='chat'),
    path('api/chat/start/', views.start_chat, name='start_chat'),
    path('api/chat/message/', views.save_chat, name='save_chat'),
    path('api/chat/end/', views.end_chat, name='end_chat'),
]
