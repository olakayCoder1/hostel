# Generated by Django 4.2.1 on 2023-08-05 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0004_hostel_has_disable'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='expiration_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]