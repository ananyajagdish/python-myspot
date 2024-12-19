# Generated by Django 5.1.3 on 2024-11-21 03:19

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('park', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='vehicle_id',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Vehicles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_number', models.CharField(max_length=25)),
                ('year', models.CharField(max_length=25)),
                ('make', models.CharField(max_length=25)),
                ('model', models.CharField(max_length=25)),
                ('over_size', models.BooleanField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'vehicles',
            },
        ),
    ]
