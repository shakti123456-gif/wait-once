# Generated by Django 4.2 on 2024-06-24 08:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Client_provider', '0024_alter_client_details_type_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='provider',
            old_name='User_add',
            new_name='Provider_employers',
        ),
    ]
