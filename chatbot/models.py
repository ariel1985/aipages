
from django.db import models
from django.contrib.auth.models import User


class Chat(models.Model):
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) # Assuming User is your user model
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

