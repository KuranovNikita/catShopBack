from urllib import response
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
import online_users.models
from .models import Dialog, Message
from  datetime  import  timedelta
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from telegramApi.models import TelegramToken
from viberApi.models import ViberToken
from accounts.models import Account
from statisticsOperator.models import StatisticsData
import requests

@login_required
def index(request):
    see_users()
    return render(request, 'chat\index.html')


def see_users():
    # pass
    user_status = online_users.models.OnlineUserActivity.get_user_activities(timedelta(seconds=60))
    print(user_status[0].user)
    print(user_status[0].last_activity)
    
    users = (user for user in user_status)
    print(users)
#   context = {"online_users"}
#   print(context)
    number_of_active_users = user_status.count()
    print(number_of_active_users)
    for i in range(0, number_of_active_users):
        print(user_status[i].user)
        print(user_status[i].last_activity)


@csrf_exempt 
def get_dialogs(request):
    data = json.loads(request.body)
    # print(data)
    # data = request.body
    operator_login = data['login']
    response = []
    dialogs = Dialog.objects.filter(operator__login=operator_login).values()
    messages = Message.objects.filter(dialog__operator__login=operator_login).values()
    # dialogs = Dialog.objects.filter(operator_name=operator_name).values()
    # messages = Message.objects.filter(dialog__operator_name=operator_name).values()
    for d in dialogs:
        d['clientName'] = d['user_name']
        d['typeDialog'] = d['type_dialog']
        d['avatarNumber'] = d['avatar_num']
        d['idChat'] = d['chat_id']
        del d['user_name']
        del d['type_dialog']
        del d['avatar_num']
        del d['chat_id']
        del d['operator_id']
        d['messages'] = []
        response.append(d)
    for m in messages:
        for d in dialogs:
            if m['dialog_id'] == d['id']:
                m['isOperator'] = m['is_operator']
                m['isRead'] = m['is_read']
                m['idMessage'] = m['id_message']
                del m['is_operator']
                del m['is_read']
                del m['id_message']
                d['messages'].append(m)
    # print(arr_message)
    # print(response)
    json.dumps(response)
    # print('/////////////////////////////////////////////////////////////////////////////')
    # print(json.dumps(response))
    # response = {}
    # response['text'] = 'text'
    return JsonResponse(json.dumps(response), safe=False)

@csrf_exempt 
def get_message_from_operator(request):
    data = json.loads(request.body)
    text = data['msg']
    chat_id = data['idChat']
    id_message = data['idMessage']
    dialog = Dialog.objects.filter(chat_id=chat_id)
    print(dialog[0])
    type_dialog = dialog[0].type_dialog
    # operator = dialog[0].operator
    # statisticOperator = StatisticsData.objects.filter(operator=operator)
    # num = statisticOperator[0].send_messages + 1
    # statisticOperator.update(send_messages=num)
    is_operator = True
    is_read = True
    create_message(dialog, text, id_message, is_operator, is_read)
    if type_dialog == 'telegram':
        send_message_to_telegram(chat_id, text)
    elif type_dialog == 'viber':
        send_message_to_viber(chat_id, text)
    return HttpResponse({"ok": True})

@csrf_exempt
def is_read_message(request):
    data = json.loads(request.body)
    id_message = data['idMessage']
    print('READ')#!!!!!!!!!!!!!!!
    message = Message.objects.filter(id_message=id_message).update(is_read=True)
    return HttpResponse({"ok": True})

@csrf_exempt
def delete_dialog(request):
    data = json.loads(request.body)
    chat_id = data['idChat']
    login = data['login']
    Dialog.objects.filter(chat_id=chat_id).delete()
    account = Account.objects.filter(login=login)
    num = account[0].active_dialogs - 1
    account.update(active_dialogs=num)
    return HttpResponse({"ok": True})

@csrf_exempt
def set_online(request):
    data = json.loads(request.body)
    login = data['login']
    online = data['online']
    account = Account.objects.filter(login=login)
    account.update(online=online)
    return HttpResponse({"ok": True})

@csrf_exempt
def check_auth(request):
    data = json.loads(request.body)
    login = data['login']
    account = Account.objects.filter(login=login)
    if account:
        if account[0].password == data['password']:
            response = {'response': 'yes'}
            response['login'] = data['login']
            response['name'] = account[0].name
            response['surname'] = account[0].surname
            # account.update(online=True)
        else:
            response = {'response': 'not password'}
    else:
        response = {'response': 'not login'}
    
    return JsonResponse(json.dumps(response), safe=False)

@csrf_exempt
def get_statistics(request):
    data = json.loads(request.body)
    login = data['login']
    statisticOperator = StatisticsData.objects.filter(login=login)
    response = {'allDialogs': statisticOperator[0].all_dialogs}
    response['sendMessage'] = statisticOperator[0].send_messages
    response['readMessage'] = statisticOperator[0].read_messages
    return JsonResponse(json.dumps(response), safe=False)


def create_new_dialog(chat_id, client_name, type_dialog, operator_name, avatar_num):
    operator = Account.objects.filter(login=operator_name)
    operator = operator[0]
    statisticOperator = StatisticsData.objects.filter(login=operator_name)
    num = statisticOperator[0].all_dialogs + 1
    statisticOperator.update(all_dialogs=num)
    new_dialog = Dialog(chat_id=chat_id, user_name=client_name, type_dialog=type_dialog, operator=operator, avatar_num=avatar_num)
    new_dialog.save()

def create_message(dialog, text, id_message, is_operator, is_read):
    print(dialog)
    dialog = dialog[0]
    operator = dialog.operator
    statisticOperator = StatisticsData.objects.filter(operator=operator)
    if is_operator:
        num = statisticOperator[0].send_messages + 1
        statisticOperator.update(send_messages=num)
    else:
        num = statisticOperator[0].read_messages + 1
        statisticOperator.update(read_messages=num)
    new_message = Message(is_operator=is_operator, text=text, dialog=dialog, id_message=id_message, is_read=is_read)
    new_message.save()

def send_message_to_telegram(chat_id, text):
    telegram_token = TelegramToken.objects.all().first()
    telegram_token = telegram_token.telegram_token
    url =f'https://api.telegram.org/bot{telegram_token}/sendMessage?chat_id={chat_id}&text={text}'
    r = requests.get(url)
    return HttpResponse({"ok": True})

def send_message_to_viber(chat_id, text):
    viber_token = ViberToken.objects.all().first()
    viber_token = viber_token.viber_token
    url = 'https://chatapi.viber.com/pa/send_message'
    header = {"Content-type": "application/json", "X-Viber-Auth-Token": viber_token}
    datar = {
        "receiver":chat_id,
        "min_api_version":1,
        "sender":{
            "name":"Operator1",
            "avatar":"http://avatar.example.com"
        },
        "tracking_data":"tracking data",
        "type":"text",
        "text":text
    }
    datar = json.dumps(datar) 
    r = requests.post(url, data=datar, headers=header)
    return HttpResponse({"ok": True})
 

def choose_operator():
    operators = Account.objects.filter(online=True)
    if len(operators) > 0:
        arr = []
        for o in operators:
            arr.append({'login': o.login, 'active_dialogs': o.active_dialogs})
        # print(arr)
        active_dialogs = 1000
        for a in arr:
            if a['active_dialogs'] < active_dialogs:
                active_dialogs = a['active_dialogs']
                operator_login = a['login']
        operatorActive = Account.objects.filter(login=operator_login)
        print(f'активный оператор {operatorActive[0]}')
        num = operatorActive[0].active_dialogs + 1
        operatorActive.update(active_dialogs=num)
        return operator_login
    else:
        return 'offline'

def avatar_num_select():
    return 1