# Generated by Django 4.2.4 on 2023-08-02 11:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productresult',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 2, 11, 57, 11, 148129)),
        ),
    ]
