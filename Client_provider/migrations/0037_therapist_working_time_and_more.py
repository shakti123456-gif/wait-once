# Generated by Django 4.2 on 2024-07-02 05:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Client_provider', '0036_therapist_unavailability_createdat_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Therapist_working_time',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('startime', models.TimeField()),
                ('endtime', models.TimeField()),
                ('createdAt', models.DateTimeField(blank=True, null=True)),
                ('updateAt', models.DateTimeField(blank=True, null=True)),
                ('therapist_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Client_provider.therapist')),
            ],
        ),
        migrations.DeleteModel(
            name='Therapist_bookeds_slots',
        ),
    ]
