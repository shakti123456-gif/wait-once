# Generated by Django 4.2 on 2024-06-20 05:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mobile_api_user', '0008_rename_firstname_user_mobile_communicationpreference_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user_mobile',
            options={'managed': True, 'verbose_name': 'Mobile user', 'verbose_name_plural': 'Mobile user'},
        ),
    ]
