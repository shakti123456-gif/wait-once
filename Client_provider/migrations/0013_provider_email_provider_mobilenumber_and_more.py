# Generated by Django 4.2 on 2024-06-22 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Client_provider', '0012_remove_location_street_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='provider',
            name='email',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='provider',
            name='mobileNumber',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='provider',
            name='ndisNumber',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
