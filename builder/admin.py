from django.contrib import admin
from .models import Pages,GrapesJSBlock, BlockCategory, MediaObject
from chatbot.models import Conversation

admin.site.register(Conversation)
admin.site.register(Pages)
admin.site.register(GrapesJSBlock)
admin.site.register(BlockCategory)
admin.site.register(MediaObject)
