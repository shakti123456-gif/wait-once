# Generated by Django 4.2 on 2024-08-07 06:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Client_provider', '0071_appointment1_istherapistchanged_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='appointment1',
            old_name='IsTherapistChanged',
            new_name='isTherapistChanged',
        ),
    ]
