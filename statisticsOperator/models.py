from django.db import models
from accounts.models import Account

class StatisticsData(models.Model):
    login = models.CharField(max_length=100, null=True)
    operator = models.ForeignKey(Account, on_delete=models.CASCADE)
    all_dialogs = models.IntegerField(null=True)
    read_messages = models.IntegerField(null=True)
    send_messages = models.IntegerField(null=True)
    
    def __str__(self):
        return self.login
