# Generated by Django 3.1 on 2020-09-25 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20200925_2227'),
    ]

    operations = [
        migrations.AddField(
            model_name='base',
            name='password2',
            field=models.CharField(default='1111', max_length=32),
        ),
    ]
