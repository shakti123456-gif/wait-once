# Generated by Django 4.2 on 2024-06-14 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mobile_api_user', '0005_user_mobile_signing_as'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_mobile',
            name='is_superuser',
            field=models.BooleanField(default=True),
        ),
    ]