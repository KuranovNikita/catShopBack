from django.urls import path
from viberApi.views import *

urlpatterns = [
    path('viberWebhook', viber_webhook),
]