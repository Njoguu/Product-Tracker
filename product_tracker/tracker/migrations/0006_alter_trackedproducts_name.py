# Generated by Django 4.2.4 on 2023-08-04 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0005_alter_productresult_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trackedproducts',
            name='name',
            field=models.CharField(max_length=1000, unique=True),
        ),
    ]