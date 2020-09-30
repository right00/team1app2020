# Generated by Django 3.1 on 2020-09-30 01:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_auto_20200930_0856'),
    ]

    operations = [
        migrations.AddField(
            model_name='students',
            name='use_base',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='teachers',
            name='use_base',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='tasks',
            name='make',
            field=models.DateField(default=datetime.datetime(2020, 9, 30, 10, 15, 11, 904554)),
        ),
    ]
