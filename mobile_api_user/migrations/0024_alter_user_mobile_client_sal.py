# Generated by Django 4.2 on 2024-06-26 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mobile_api_user', '0023_remove_client_details_view_client_sal_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_mobile',
            name='Client_Sal',
            field=models.CharField(blank=True, default='Mr', max_length=1, null=True),
        ),
    ]
