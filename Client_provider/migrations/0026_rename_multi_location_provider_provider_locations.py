# Generated by Django 4.2 on 2024-06-24 08:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Client_provider', '0025_rename_user_add_provider_provider_employers'),
    ]

    operations = [
        migrations.RenameField(
            model_name='provider',
            old_name='multi_location',
            new_name='Provider_locations',
        ),
    ]
