# Generated by Django 4.2 on 2024-08-02 04:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Client_provider', '0063_rename_usertype_provider_employee_usertype'),
    ]

    operations = [
        migrations.CreateModel(
            name='therapistPostReoccurAppoinment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AddField(
            model_name='appointment1',
            name='createdAt',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='appointment1',
            name='lastUpdate',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
