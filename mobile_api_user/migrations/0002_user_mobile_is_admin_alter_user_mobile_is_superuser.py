# Generated by Django 4.2 on 2024-06-07 03:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mobile_api_user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_mobile',
            name='is_admin',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='user_mobile',
            name='is_superuser',
            field=models.BooleanField(default=True),
        ),
    ]
