
from django.db import models
from django.contrib.auth.models import User


class Conversation(models.Model):
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(User, on_delete=models.CASCADE) # Assuming User is your user model
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

