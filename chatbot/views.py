from django.shortcuts import render
from django.http import JsonResponse, HttpResponseNotAllowed
from .models import Conversation
import requests

# from django.views.decorators.csrf import csrf_exempt


def chat_view(request):
    return render(request, 'chatbot/chat.html')

# to test from curl only:
# @csrf_exempt
def api_chat(request):
    if request.method == "POST":
        user_message = request.POST.get('message')
        
        # Sending the message to Rasa
        response = requests.post('http://localhost:5005/webhooks/rest/webhook', json={
            'sender': 'user',
            'message': user_message
        })
        rasa_data = response.json()
        bot_response = rasa_data[0]['text'] if rasa_data and len(rasa_data) > 0 else 'No answer'
        try:
            # Save the conversation to the database
            Conversation.objects.create(user_message=user_message, bot_response=bot_response)
        except Exception as e:
            print(f"Error saving conversation: {e}")
            # Optionally, send back an error response or handle the exception as needed
        
        return JsonResponse({'response': bot_response})
    else:
        return HttpResponseNotAllowed(['POST'], "This endpoint only supports POST requests.")
