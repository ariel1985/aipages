
from django.utils import timezone # from datetime import timezone was no good for django
import json
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseNotAllowed
from .models import Chat
import requests

# from django.views.decorators.csrf import csrf_exempt # to test from curl only:


def chat_view(request):
    # Create a new Chat instance when the chat page is loaded
    chat = Chat.objects.create()
    request.session['chat_id'] =chat.id  # Store chat ID in session
    return render(request, 'chatbot/chat.html', {'chat_id': chat.id})


# to test from curl only:
# @csrf_exempt
from .models import Message, Chat

def save_chat(request):
    if request.method == "POST":
        
        data = json.loads(request.body.decode("utf-8"))
        chat_id = data.get('chat_id')
        user_message = data.get('message')

        # Validate chat exists and type
        try:
            chat = Chat.objects.get(pk=int(chat_id))
        except ValueError:
            return JsonResponse({'error': 'Invalid chat_id format. Expected an integer.'}, status=400)
        except Chat.DoesNotExist:
            return JsonResponse({'error': 'Invalid chat_id'}, status=400)


        # Sending the message to Rasa
        response = requests.post('http://localhost:5005/webhooks/rest/webhook', json={
            'sender': 'user',
            'message': user_message
        })
        
        rasa_data = response.json()
        bot_response = rasa_data[0]['text'] if rasa_data and len(rasa_data) > 0 else 'No answer'

        try:
            # Save the user's message
            Message.objects.create(
                chat=chat,
                user=request.user,  # assuming you have authentication in place
                content=user_message
            )

            # Save the bot's response
            Message.objects.create(
                chat=chat,
                user=None,  # bot messages can have user set to None or a dedicated bot user
                content=bot_response
            )

        except Exception as e:
            print(f"Error saving messages: {e}")
            # Optionally, send back an error response or handle the exception as needed
        
        return JsonResponse({'response': bot_response})
    else:
        return HttpResponseNotAllowed(['POST'], "This endpoint only supports POST requests.")


def start_chat(request):
    if request.method == 'POST':
        new_chat = Chat.objects.create()
        return JsonResponse({'chat_id': new_chat.id})
    
# @csrf_exempt
def end_chat(request):
    if request.method == "POST":
        
        data = json.loads(request.body.decode("utf-8"))
        chat_id = data.get('chat_id')
        
        chat = Chat.objects.get(pk=chat_id)
        chat.end_date = timezone.now()
        chat.save()
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "error"})