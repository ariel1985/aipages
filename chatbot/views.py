
from django.utils import timezone # from datetime import timezone was no good for django
import json
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseNotAllowed
from .models import Message, Chat
import requests
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt # to test from curl only:



def chat_button(request):
    return render(request, 'chatbot/chat_button.html')


def chat_view(request):
    # Create a new Chat instance when the chat page is loaded
    # chat = Chat.objects.create()
    # request.session['chat_id'] =chat.id  # Store chat ID in session
    # return render(request, 'chatbot/chat.html', {'chat_id': 0})
    return render(request, 'chatbot/chat.html')


def view_chats(request):
    # Initial chats queryset
    chats_list = Chat.objects.all().order_by('-id')

    # Filtering based on GET parameters
    chat_id = request.GET.get('chat_id')
    user_name = request.GET.get('user_name')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    message_content = request.GET.get('message_content')

    if chat_id:
        chats_list = chats_list.filter(id=chat_id)
    if user_name:
        chats_list = chats_list.filter(messages__user__username__icontains=user_name).distinct()
    if start_date:
        chats_list = chats_list.filter(start_date__date=start_date)
    if end_date:
        chats_list = chats_list.filter(end_date__date=end_date)
    if message_content:
        chats_list = chats_list.filter(messages__content__icontains=message_content).distinct()

    # Pagination
    num_per_page = 15 # Show 10 chats per page
    paginator = Paginator(chats_list, num_per_page)  
    page_number = request.GET.get('page')
    chats = paginator.get_page(page_number)

    for chat in chats:
        first_message = chat.messages.first()
        if first_message:
            chat.user_name = first_message.user.username
        else:
            chat.user_name = "Unknown"
        chat.message_count = chat.messages.count()

    return render(request, 'chatbot/chats.html', {'chats': chats})

def view_chat(request, chat_id):
    try:
        chat = Chat.objects.get(pk=chat_id)
        messages = chat.messages.all().order_by('timestamp')
        chat_data = [{"user": msg.user.username if msg.user else "Bot", "content": msg.content} for msg in messages]
        return render(request, 'chatbot/chat.html', {'chat_data': chat_data, 'chat_id': chat_id})

    except Chat.DoesNotExist:
        return JsonResponse({'error': 'Chat not found'}, status=404)

# TODO: This should not be in production
@csrf_exempt 
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
        print(' -- HERE COMES THE DATA --')
        print(rasa_data)
        print(' ---- IM A LIVING LIFE GANGSTA ---')
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
        
        return JsonResponse({'response': bot_response, 'rasa_data': rasa_data})
    else:
        return HttpResponseNotAllowed(['POST'], "This endpoint only supports POST requests.")

@csrf_exempt # TODO: This should not be in production
def start_chat(request):
    if request.method == 'POST':
        new_chat = Chat.objects.create()
        return JsonResponse({'chat_id': new_chat.id})
    else:
        return HttpResponseNotAllowed(['POST'])  # Indicates that only POST is allowed
  
@csrf_exempt # TODO: This should not be in production
def end_chat(request):
    if request.method == "POST":
        
        data = json.loads(request.body.decode("utf-8"))
        chat_id = data.get('chat_id')
        
        chat = Chat.objects.get(pk=chat_id)
        chat.end_date = timezone.now()
        chat.save()
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "error"})