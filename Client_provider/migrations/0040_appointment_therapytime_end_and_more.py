# Generated by Django 4.2 on 2024-07-03 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Client_provider', '0039_rename_isconfirmed_appointment_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='TherapyTime_end',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='appointment',
            name='TherapyTime_start',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='appointmentDate',
            field=models.DateField(blank=True, null=True),
        ),
    ]
