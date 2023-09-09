from django.urls import reverse
import json
import requests_mock
from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Chat, Message

class ChatTestCase(TestCase):
    def setUp(self):
        # You may also want to set up a test user or other related objects here.
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_chat_flow(self):
        # Login
        self.client.login(username='testuser', password='testpassword')

        # 1. Start a chat
        response = self.client.post('/chatbot/api/chat/start/')
        self.assertEqual(response.status_code, 200)
        chat_id = response.json().get('chat_id')
        self.assertIsNotNone(chat_id)

        # Verify chat is created
        chat = Chat.objects.get(pk=chat_id)
        self.assertIsNotNone(chat)

        # 2. Send a message
        user_message = "Hello"
        response = self.client.post('/chatbot/api/chat/message/', data={
            'chat_id': chat_id,
            'message': user_message
        }, content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        bot_response = response.json().get('response')
        self.assertIsNotNone(bot_response)

        # Verify both user and bot messages are stored
        user_msg_instance = Message.objects.filter(chat=chat, user=self.user, content=user_message).first()
        bot_msg_instance = Message.objects.filter(chat=chat, user__isnull=True, content=bot_response).first()
        self.assertIsNotNone(user_msg_instance)
        self.assertIsNotNone(bot_msg_instance)

        # 3. End the chat
        response = self.client.post('/chatbot/api/chat/end/', data={
            'chat_id': chat_id
        }, content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        status = response.json().get('status')
        self.assertEqual(status, "success")

        # Verify chat has ended
        chat.refresh_from_db()
        self.assertIsNotNone(chat.end_date)



'''
This test does the following:

Mocks the Rasa framework's response using requests_mock to simulate a successful message response.
Sends a message to save_chat via a POST request.
Checks if the received response matches the mocked Rasa's response.
Queries the database to check if the Chat (user message and bot response) is saved correctly.

'''

# class ApiChatTestCase(TestCase):

#     def test_save_chat_response_and_db_save(self):
#         # Mock Rasa's response
#         rasa_response = [{"text": "Hello tester"}]
#         with requests_mock.Mocker() as m:
#             m.post("http://localhost:5005/webhooks/rest/webhook", json=rasa_response)

#             # Send message to save_chat as JSON string
#             post_data = json.dumps({"message": "Hello"})
#             response = self.client.post(reverse('chatbot:save_chat'), data=post_data, content_type='application/json')

#             # Check if the response status is 200 OK
#             self.assertEqual(response.status_code, 200)

#             # Check if the response contains the mocked Rasa's response
#             self.assertEqual(response.json()['response'], rasa_response[0]['text'])

#             # Check if the chat is saved to the database
#             saved_chat = Chat.objects.last()
#             self.assertIsNotNone(saved_chat)
#             # I assume you have attributes like `user_message` and `bot_response` in your Chat model
#             # If not, adjust the below lines according to your model's attributes
#             self.assertEqual(saved_chat.user_message, "Hello tester")
#             self.assertEqual(saved_chat.bot_response, rasa_response[0]['text'])