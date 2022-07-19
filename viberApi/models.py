from django.db import models

# Create your models here.
class ViberToken(models.Model):
    viber_token = models.CharField(max_length=300)

    def __str__(self):
        return self.viber_token

