# Generated by Django 4.2 on 2024-07-05 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Client_provider', '0045_rename_provider_appointment_providerid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='TherapyTime_end',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='TherapyTime_start',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
