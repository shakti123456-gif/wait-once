# Generated by Django 4.2 on 2024-06-14 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User_mobile',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('signing_as', models.CharField(choices=[('Self', 'Self'), ('Parent', 'Parent')], default='Self', max_length=6)),
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(blank=True, max_length=100, null=True)),
                ('last_name', models.CharField(blank=True, max_length=100, null=True)),
                ('Dateofbirth', models.DateField(blank=True, null=True)),
                ('mobile_number', models.CharField(max_length=15, unique=True)),
                ('email_address', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('ndis_number', models.CharField(blank=True, max_length=15, null=True, unique=True)),
                ('Language_perfered', models.CharField(blank=True, max_length=100, null=True)),
                ('Refferal_code', models.CharField(blank=True, max_length=50, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=True)),
                ('is_superuser', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('password', models.CharField(max_length=15)),
            ],
            options={
                'db_table': 'mobile_api_user_user_mobile',
                'managed': True,
            },
        ),
    ]
