# Generated by Django 4.2.4 on 2023-08-02 13:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0002_alter_productresult_created_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrackedProducts',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=1000)),
                ('created_at', models.DateTimeField(default=datetime.datetime(2023, 8, 2, 13, 17, 46, 518122))),
                ('tracked', models.BooleanField(default=True)),
            ],
        ),
        migrations.AlterField(
            model_name='productresult',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 2, 13, 17, 46, 517093)),
        ),
    ]
