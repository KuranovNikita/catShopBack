# Generated by Django 4.0.2 on 2022-07-15 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_account'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='surname',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
