# Generated by Django 4.2 on 2024-07-23 10:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Client_provider', '0054_therapistavailability_availableslotsdata_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='appointment1',
            old_name='LocationId',
            new_name='Locationdata',
        ),
        migrations.RenameField(
            model_name='appointment1',
            old_name='clientId',
            new_name='clientdata',
        ),
        migrations.RenameField(
            model_name='appointment1',
            old_name='providerId',
            new_name='providerdata',
        ),
        migrations.RenameField(
            model_name='appointment1',
            old_name='serviceId',
            new_name='servicedata',
        ),
        migrations.RenameField(
            model_name='appointment1',
            old_name='therapistId',
            new_name='therapistdata',
        ),
    ]
