# Generated by Django 4.2 on 2024-08-08 19:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Client_provider', '0076_clientprebookappointments_therapyslot'),
    ]

    operations = [
        migrations.RenameField(
            model_name='appointment',
            old_name='isconfimed',
            new_name='isConfirmed',
        ),
        migrations.RenameField(
            model_name='appointment1',
            old_name='isconfimed',
            new_name='isConfirmed',
        ),
        migrations.RenameField(
            model_name='reoccureappointments',
            old_name='isconfimed',
            new_name='isConfirmed',
        ),
    ]
