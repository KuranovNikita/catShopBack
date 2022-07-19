# Generated by Django 4.0.2 on 2022-02-16 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ViberDialog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('viber_chat_id', models.CharField(max_length=300, null=True)),
                ('viber_user_name', models.CharField(max_length=300, null=True)),
                ('operator_id', models.CharField(max_length=300, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ViberToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('viber_token', models.CharField(max_length=300)),
            ],
        ),
    ]
