# Generated by Django 4.2 on 2024-08-09 06:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mobile_api_user', '0035_client_sub_view_insurancetype'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user_mobile',
            old_name='firebaseKey',
            new_name='fireBaseKey',
        ),
    ]
