# Generated by Django 4.2.1 on 2023-08-05 09:51

import account.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_transaction_status_alter_user_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(blank=True, help_text='', null=True, upload_to=account.models.upload_to),
        ),
    ]