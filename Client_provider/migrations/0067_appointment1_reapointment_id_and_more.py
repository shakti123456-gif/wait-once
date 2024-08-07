# Generated by Django 4.2 on 2024-08-06 19:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Client_provider', '0066_remove_clientprebookappointments_therapist_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment1',
            name='reapointment_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='clientprebookappointments',
            name='serviceData',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Client_provider.service'),
        ),
    ]