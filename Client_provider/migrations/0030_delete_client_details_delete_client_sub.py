# Generated by Django 4.2 on 2024-06-24 11:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Client_provider', '0029_rename_phone_2_provider_phoneno'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Client_details',
        ),
        migrations.DeleteModel(
            name='Client_sub',
        ),
    ]