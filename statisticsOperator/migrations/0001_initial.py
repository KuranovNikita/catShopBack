# Generated by Django 4.0.2 on 2022-07-18 16:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0004_account_active_dialogs_account_online'),
    ]

    operations = [
        migrations.CreateModel(
            name='StatisticsData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('all_dialogs', models.IntegerField(null=True)),
                ('read_messages', models.IntegerField(null=True)),
                ('operator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.account')),
            ],
        ),
    ]
