# Generated by Django 4.2 on 2024-08-08 06:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Client_provider', '0073_alter_clientprebookappointments_options_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reoccureappointments',
            old_name='reoccurAppointmentValid',
            new_name='reoccurAppointmentDetail',
        ),
    ]