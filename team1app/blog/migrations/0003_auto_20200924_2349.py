# Generated by Django 3.1 on 2020-09-24 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20200917_0522'),
    ]

    operations = [
        migrations.AddField(
            model_name='base',
            name='password',
            field=models.CharField(default='0000', max_length=32),
        ),
        migrations.AddField(
            model_name='classes',
            name='password',
            field=models.CharField(default=0, max_length=32),
        ),
    ]