# Generated by Django 4.2 on 2024-07-03 04:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mobile_api_user', '0028_rename_add_caretaker_detail_client_details_view_addchildren_and_more'),
        ('Client_provider', '0037_therapist_working_time_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='appointment',
            options={'managed': True, 'verbose_name': 'Schedules', 'verbose_name_plural': 'Schedules'},
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='Location_id',
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='therapy_end_time',
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='therapy_start_time',
        ),
        migrations.AddField(
            model_name='appointment',
            name='appointmentDate',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='appointment',
            name='childId',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mobile_api_user.client_sub_view'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='clientId',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='appointment',
            name='isConfirmed',
            field=models.CharField(choices=[('waiting', 'Waiting'), ('confirmed', 'Confirmed')], default='waiting', max_length=10),
        ),
    ]
