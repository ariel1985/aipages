from django.test import TestCase
from django.urls import reverse
import requests_mock
from .models import Conversation

'''
This test does the following:

Mocks the Rasa framework's response using requests_mock to simulate a successful message response.
Sends a message to save_chat via a POST request.
Checks if the received response matches the mocked Rasa's response.
Queries the database to check if the conversation (user message and bot response) is saved correctly.

'''
class ApiChatTestCase(TestCase):

    def test_save_chat_response_and_db_save(self):
        # Mock Rasa's response
        rasa_response = [{"text": "Hello tester"}]
        with requests_mock.Mocker() as m:
            m.post("http://localhost:5005/webhooks/rest/webhook", json=rasa_response)

            # Send message to save_chat
            response = self.client.post(reverse('chatbot:save_chat'), data={"message": "Hello"})

            # Check if the response status is 200 OK
            self.assertEqual(response.status_code, 200)

            # Check if the response contains the mocked Rasa's response
            self.assertEqual(response.json()['response'], rasa_response[0]['text'])

            # Check if the conversation is saved to the database
            saved_conversation = Conversation.objects.last()
            self.assertIsNotNone(saved_conversation)
            self.assertEqual(saved_conversation.user_message, "Hello tester")
            self.assertEqual(saved_conversation.bot_response, rasa_response[0]['text'])

