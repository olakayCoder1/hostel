# Generated by Django 4.2.1 on 2023-08-06 11:29

import account.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0021_alter_profile_phone_number_alter_user_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(blank=True, help_text='', null=True, upload_to=account.models.upload_to),
        ),
    ]