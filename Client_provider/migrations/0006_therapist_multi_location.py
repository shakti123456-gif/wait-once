# Generated by Django 4.2 on 2024-06-20 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Client_provider', '0005_remove_provider_multi_location_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='therapist',
            name='multi_Location',
            field=models.ManyToManyField(to='Client_provider.location'),
        ),
    ]
