from django.contrib import admin
from .models import User, Message, GroupMember, Conversation
# Register your models here.
admin.site.register(User)
admin.site.register(Message)
admin.site.register(GroupMember)
admin.site.register(Conversation)