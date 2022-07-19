from django.contrib import admin

from .models import Dialog, Message

admin.site.register(Message)
admin.site.register(Dialog)
