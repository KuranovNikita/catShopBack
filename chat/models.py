from django.db import models
from accounts.models import Account

class Dialog(models.Model):
    chat_id = models.CharField(max_length=200, null=True)
    user_name = models.CharField(max_length=200, null=True)
    avatar_num = models.CharField(max_length=10, null=True)
    operator = models.ForeignKey(Account, on_delete=models.CASCADE)
    type_dialog = models.CharField(max_length=50, null=True)
    
    def __str__(self):
        return self.user_name

class Message(models.Model):
    is_operator = models.BooleanField(null=True)
    text = models.CharField(max_length=4096, null=True)
    id_message = models.CharField(max_length=128, null=True)
    is_read = models.BooleanField(null=True)
    dialog = models.ForeignKey(Dialog, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.text