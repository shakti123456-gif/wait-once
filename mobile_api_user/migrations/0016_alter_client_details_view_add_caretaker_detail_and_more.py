# Generated by Django 4.2 on 2024-06-24 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mobile_api_user', '0015_client_sub_view_delete_client_sub_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client_details_view',
            name='Add_Caretaker_Detail',
            field=models.ManyToManyField(blank=True, null=True, to='mobile_api_user.client_sub_view'),
        ),
        migrations.AlterField(
            model_name='client_details_view',
            name='Client_Sal',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='client_details_view',
            name='Type',
            field=models.CharField(blank=True, choices=[('M', 'M'), ('F', 'F')], max_length=1, null=True),
        ),
    ]
