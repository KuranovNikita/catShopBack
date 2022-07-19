# Generated by Django 4.0.2 on 2022-07-18 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_account_surname'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='active_dialogs',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='account',
            name='online',
            field=models.BooleanField(null=True),
        ),
    ]