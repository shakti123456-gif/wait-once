# Generated by Django 4.2 on 2024-08-06 22:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Client_provider', '0067_appointment1_reapointment_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment1',
            name='reapointment_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Client_provider.clientprebookappointments'),
        ),
    ]
