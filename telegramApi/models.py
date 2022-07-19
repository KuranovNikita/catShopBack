from django.db import models

# Create your models here.
class TelegramToken(models.Model):
    telegram_token = models.CharField(max_length=300)

    def __str__(self):
        return self.telegram_token



