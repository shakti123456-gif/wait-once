# Generated by Django 4.2 on 2024-06-25 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mobile_api_user', '0019_alter_client_details_view_client_auth_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client_sub_view',
            name='dateofbirth',
            field=models.DateField(blank=True, null=True),
        ),
    ]
