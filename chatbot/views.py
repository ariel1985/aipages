import json
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseNotAllowed
from .models import Conversation
import requests

# from django.views.decorators.csrf import csrf_exempt # to test from curl only:


def chat_view(request):
    # Create a new Conversation instance when the chat page is loaded
    conversation = Conversation.objects.create()
    request.session['conversation_id'] = conversation.id  # Store conversation ID in session
    return render(request, 'chatbot/chat.html', {'conversation_id': conversation.id})


# to test from curl only:
# @csrf_exempt
from .models import Message, Conversation

def save_chat(request):
    if request.method == "POST":
        
        # user_message = request.POST.get('message')
        # conversation_id = request.POST.get('conversation_id')  # Expect the frontend to send the conversationId
        
        data = json.loads(request.body.decode("utf-8"))
        conversation_id = data.get('conversation_id')
        user_message = data.get('message')

        # Validate conversation exists and type
        try:
            conversation = Conversation.objects.get(pk=int(conversation_id))
        except ValueError:
            return JsonResponse({'error': 'Invalid conversation_id format. Expected an integer.'}, status=400)
        except Conversation.DoesNotExist:
            return JsonResponse({'error': 'Invalid conversation_id'}, status=400)


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
                conversation=conversation,
                user=request.user,  # assuming you have authentication in place
                content=user_message
            )

            # Save the bot's response
            Message.objects.create(
                conversation=conversation,
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
        new_conversation = Conversation.objects.create()
        return JsonResponse({'conversation_id': new_conversation.id})
    
# @csrf_exempt
def end_chat(request):
    if request.method == "POST":
        data = json.loads(request.body)
        conversation_id = data.get('conversation_id')
        conversation = Conversation.objects.get(pk=conversation_id)
        conversation.end_date = timezone.now()
        conversation.save()
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "error"})