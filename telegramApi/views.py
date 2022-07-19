from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import TelegramToken
from chat.models import Dialog, Message
from chat.views import choose_operator, avatar_num_select, create_new_dialog, create_message, send_message_to_telegram

import json
import requests

@csrf_exempt 
def telegram_webhook(request):
    # print('TELEGRAMMM!!!!!')
    data = json.loads(request.body)
    # print(data)
    chat_id = data['message']['from']['id']
    id_message = data['update_id']
    text = data['message']['text']
    dialog = Dialog.objects.filter(chat_id=chat_id)
    is_operator = False
    is_read = False
    if not dialog:
        # print('NEWDIALOG')
        create_new_telegram_dialog(data, dialog, text, id_message, is_operator, is_read, chat_id)
        # create_message(dialog, text, id_message, is_operator, is_read)
    else:
        print(f'dialog_id = {dialog[0].id}')
        create_message(dialog, text, id_message, is_operator, is_read)
    return HttpResponse({"ok": True})

def create_new_telegram_dialog(data, dialog, text, id_message, is_operator, is_read, chat_id):
    operator_name = choose_operator()
    if operator_name == 'offline':
        text = 'В данный момент нет операторов онлайн, обратитесь в часы работы операторов.'
        send_message_to_telegram(chat_id, text)
        # print(operator_name)
    else:
        avatar_num = avatar_num_select()
        fromTelegram = data['message']['from']
        chat_id = fromTelegram['id']
        first_name = ''
        last_name = ''
        if 'first_name' in fromTelegram:
            first_name = fromTelegram['first_name']
        if 'last_name' in fromTelegram:
            last_name = fromTelegram['last_name']
        client_name = f'{first_name} {last_name}'
        create_new_dialog(chat_id, client_name, 'telegram', operator_name, avatar_num)
        create_message(dialog, text, id_message, is_operator, is_read)







