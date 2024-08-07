# Generated by Django 4.2 on 2024-07-05 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Client_provider', '0047_alter_appointment_therapytime_end_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clientId', models.IntegerField(blank=True, null=True)),
                ('childId', models.IntegerField(blank=True, null=True)),
                ('providerId', models.IntegerField(blank=True, null=True)),
                ('therapistId', models.IntegerField(blank=True, null=True)),
                ('serviceId', models.IntegerField(blank=True, null=True)),
                ('appointmentDate', models.DateField(blank=True, null=True)),
                ('TherapyTime_start', models.TimeField(blank=True, null=True)),
                ('TherapyTime_end', models.TimeField(blank=True, null=True)),
                ('Location_details', models.CharField(blank=True, max_length=250, null=True)),
                ('status', models.CharField(choices=[('waiting', 'Waiting'), ('confirmed', 'Confirmed')], default='waiting', max_length=10)),
                ('isconfimed', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Schedules by object',
                'verbose_name_plural': 'Schedules by object',
                'managed': True,
            },
        ),
    ]
