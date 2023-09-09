from django.db import models

class Conversation(models.Model):
    user_message = models.TextField()
    bot_response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


#  you might wanna do : 
'''
# https://chat.openai.com/share/b54a7a4b-3eb0-4f7a-bd4a-a6c2a48322c0
from django.db import models

class Conversation(models.Model):
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(User, on_delete=models.CASCADE) # Assuming User is your user model
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

'''

