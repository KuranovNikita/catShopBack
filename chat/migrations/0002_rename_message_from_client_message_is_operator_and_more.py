# Generated by Django 4.0.2 on 2022-07-11 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='message_from_client',
            new_name='is_operator',
        ),
        migrations.AddField(
            model_name='message',
            name='id_message',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='message',
            name='is_read',
            field=models.BooleanField(null=True),
        ),
    ]
