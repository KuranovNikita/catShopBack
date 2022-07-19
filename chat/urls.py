from django.http import HttpResponse
from django.urls import path
from chat.views import *

urlpatterns = [
    path('', index),
    path('getDialogs', get_dialogs),
    path('getMessageFromOperator', get_message_from_operator),
    path('isReadMessage', is_read_message),
    path('checkAuth', check_auth),
    path('deleteDialog', delete_dialog),
    path('setOnline', set_online),
    path('getStatistics', get_statistics),
          
]