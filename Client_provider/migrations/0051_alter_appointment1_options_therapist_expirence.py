# Generated by Django 4.2 on 2024-07-15 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Client_provider', '0050_alter_appointment1_clientid'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='appointment1',
            options={'managed': True, 'verbose_name': 'Apointments', 'verbose_name_plural': 'Apointments'},
        ),
        migrations.AddField(
            model_name='therapist',
            name='expirence',
            field=models.PositiveIntegerField(default=1),
        ),
    ]