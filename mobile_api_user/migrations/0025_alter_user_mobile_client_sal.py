# Generated by Django 4.2 on 2024-06-27 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mobile_api_user', '0024_alter_user_mobile_client_sal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_mobile',
            name='Client_Sal',
            field=models.CharField(blank=True, default='Mr', max_length=10, null=True),
        ),
    ]
