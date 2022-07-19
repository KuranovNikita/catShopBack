from django.urls import path
from telegramApi.views import *

urlpatterns = [
    path('telegramWebhook', telegram_webhook),
]