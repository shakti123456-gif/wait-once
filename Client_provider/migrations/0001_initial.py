# Generated by Django 4.2 on 2024-06-20 05:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Baseclass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Alternative_mobile_number', models.CharField(max_length=100)),
                ('Permanent_Address_1', models.CharField(max_length=255)),
                ('Permanent_Address_2', models.CharField(blank=True, max_length=255, null=True)),
                ('City', models.CharField(max_length=50)),
                ('State', models.CharField(max_length=50)),
                ('PIN', models.CharField(max_length=10)),
                ('Additional_Info1', models.TextField(blank=True, null=True)),
                ('Additional_Info2', models.TextField(blank=True, null=True)),
                ('Additional_Info3', models.TextField(blank=True, null=True)),
                ('Additional_Info4', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Client_sub',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('dateofbirth', models.DateTimeField()),
                ('Ndisnumber', models.CharField(max_length=20)),
            ],
            options={
                'verbose_name': 'Client sub',
                'verbose_name_plural': 'Client sub',
                'db_table': '',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('location_id', models.AutoField(primary_key=True, serialize=False)),
                ('location_num', models.CharField(max_length=100)),
                ('location_name', models.CharField(max_length=100)),
                ('location_type', models.CharField(max_length=50)),
                ('location_description', models.TextField(blank=True, null=True)),
                ('street_number', models.CharField(blank=True, max_length=10, null=True)),
                ('unit_number', models.CharField(blank=True, max_length=10, null=True)),
                ('street_name', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=50)),
                ('pin', models.CharField(max_length=10)),
                ('phone_number', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('service_id', models.AutoField(primary_key=True, serialize=False)),
                ('service_num', models.IntegerField()),
                ('service_name', models.CharField(max_length=100)),
                ('service_type', models.CharField(max_length=100)),
                ('service_description', models.CharField(max_length=128)),
                ('session_type', models.CharField(max_length=16)),
                ('session_duration', models.IntegerField()),
                ('plan_duration', models.IntegerField()),
                ('plan_type', models.CharField(max_length=8)),
                ('category', models.CharField(max_length=8)),
                ('age_group', models.CharField(max_length=8)),
                ('prerequisites', models.CharField(max_length=128)),
                ('information', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('provider_id', models.AutoField(primary_key=True, serialize=False)),
                ('provider_num', models.IntegerField()),
                ('provider_name', models.CharField(max_length=64)),
                ('provider_type', models.CharField(max_length=16)),
                ('abn', models.CharField(max_length=16)),
                ('age_group', models.CharField(max_length=16)),
                ('dva', models.CharField(blank=True, max_length=16, null=True)),
                ('chain', models.CharField(blank=True, max_length=16, null=True)),
                ('multi_location', models.CharField(blank=True, max_length=16, null=True)),
                ('phone_2', models.CharField(blank=True, max_length=16, null=True)),
                ('web', models.URLField(blank=True, max_length=128, null=True)),
                ('provider_auth', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('service_add', models.ManyToManyField(to='Client_provider.service')),
            ],
        ),
        migrations.CreateModel(
            name='Therapist',
            fields=[
                ('baseclass_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, to='Client_provider.baseclass')),
                ('therapist_id', models.AutoField(primary_key=True, serialize=False)),
                ('therapist_num', models.CharField(max_length=100)),
                ('therapist_sal', models.CharField(max_length=10)),
                ('therapist_type', models.CharField(max_length=50)),
                ('abn', models.CharField(blank=True, max_length=20, null=True)),
                ('service_age_group', models.CharField(blank=True, max_length=50, null=True)),
                ('dva', models.BooleanField(default=False)),
                ('independent', models.BooleanField(default=False)),
                ('multi_provider', models.BooleanField(default=False)),
                ('web', models.URLField(blank=True, null=True)),
                ('therapist_auth', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            bases=('Client_provider.baseclass',),
        ),
        migrations.CreateModel(
            name='Client_details',
            fields=[
                ('baseclass_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, to='Client_provider.baseclass')),
                ('Client_ID', models.AutoField(primary_key=True, serialize=False)),
                ('Client_Number', models.IntegerField()),
                ('Client_Sal', models.CharField(max_length=5)),
                ('Type', models.CharField(choices=[('M', 'M'), ('K', 'k')], max_length=1)),
                ('Add_Caretaker_Detail', models.ManyToManyField(to='Client_provider.client_sub')),
                ('Client_auth', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Client details',
                'verbose_name_plural': 'Client details',
                'db_table': '',
                'managed': True,
            },
            bases=('Client_provider.baseclass',),
        ),
    ]
