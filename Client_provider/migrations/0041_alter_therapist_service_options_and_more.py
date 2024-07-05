# Generated by Django 4.2 on 2024-07-03 06:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Client_provider', '0040_appointment_therapytime_end_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='therapist_service',
            options={'managed': True, 'verbose_name': 'therapist provide Service', 'verbose_name_plural': 'therapist provide Service'},
        ),
        migrations.AlterModelOptions(
            name='therapist_unavailability',
            options={'managed': True, 'verbose_name': 'therapist unavailbilty', 'verbose_name_plural': 'therapist unavailbilty'},
        ),
        migrations.AlterModelOptions(
            name='therapist_working_time',
            options={'managed': True, 'verbose_name': 'therapist working Time', 'verbose_name_plural': 'therapist working time'},
        ),
        migrations.AlterModelOptions(
            name='therapistavailability',
            options={'managed': True, 'verbose_name': 'therapistAvailability', 'verbose_name_plural': 'therapistAvailability'},
        ),
        migrations.AlterUniqueTogether(
            name='therapist_service',
            unique_together=set(),
        ),
    ]
