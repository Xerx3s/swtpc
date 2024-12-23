# Generated by Django 4.1.3 on 2024-12-05 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SODISForecastData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.FloatField(default='0.0')),
                ('longitude', models.FloatField(default='0.0')),
                ('starting_hour', models.IntegerField(default='8')),
                ('water_temperature', models.IntegerField(default='18')),
                ('target_logdis', models.IntegerField(default='4')),
            ],
        ),
    ]
