from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ViberToken
from chat.models import Dialog, Message
from chat.views import choose_operator, avatar_num_select, create_new_dialog, create_message, send_message_to_viber
import json
import requests

@csrf_exempt 
def viber_webhook(request):
    print('VIBER!!!!!')
    data = json.loads(request.body)
    print(data)
    event = data['event']
    if event == 'message':
        chat_id = data['sender']['id']
        text = data['message']['text']
        id_message = data['message_token']
        dialog = Dialog.objects.filter(chat_id=chat_id)
        is_operator = False
        is_read = False
        if not dialog:
            print('NEWDIALOG')
            create_new_viber_dialog(data, dialog, text, id_message, is_operator, is_read, chat_id)
            # create_message(dialog, text, id_message, is_operator, is_read)
        else:
            create_message(dialog, text, id_message, is_operator, is_read)
    return HttpResponse({"ok": True})

def create_new_viber_dialog(data, dialog, text, id_message, is_operator, is_read, chat_id):
    operator_name = choose_operator()
    if operator_name == 'offline':
        text = 'В данный момент нет операторов онлайн, обратитесь в часы работы операторов.'
        send_message_to_viber(chat_id, text)
        # print(operator_name)
    else:
        avatar_num = avatar_num_select()
        chat_id = data['sender']['id']
        client_name = data['sender']['name']
        create_new_dialog(chat_id, client_name, 'viber', operator_name, avatar_num)
        create_message(dialog, text, id_message, is_operator, is_read)



