# Generated by Django 4.2 on 2024-06-24 08:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Client_provider', '0028_alter_provider_provider_num'),
    ]

    operations = [
        migrations.RenameField(
            model_name='provider',
            old_name='phone_2',
            new_name='phoneNo',
        ),
    ]
