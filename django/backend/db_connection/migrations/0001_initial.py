# Generated by Django 4.1.3 on 2022-11-24 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='flocculation_data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('surface_water', models.CharField(default='', max_length=50)),
                ('initial_pH', models.FloatField(default='', max_length=50)),
                ('initial_EC', models.IntegerField(default='', max_length=50)),
                ('initial_turbidity', models.IntegerField(default='', max_length=50)),
                ('flocculant', models.CharField(default='', max_length=50)),
                ('floc_dose', models.IntegerField(default='', max_length=50)),
                ('floc_concentration', models.FloatField(default='', max_length=50)),
                ('floc_saline_Molarity', models.FloatField(default='', max_length=50)),
                ('floc_cactus_share', models.FloatField(default='', max_length=50)),
                ('floc_vol', models.FloatField(default='', max_length=50)),
                ('saline_concentration', models.FloatField(default='', max_length=50)),
                ('final_pH', models.FloatField(default='', max_length=50)),
                ('final_EC', models.IntegerField(default='', max_length=50)),
                ('final_turbidity', models.IntegerField(default='', max_length=50)),
                ('cal_final_EC', models.FloatField(default='', max_length=50)),
                ('delta_EC', models.FloatField(default='', max_length=50)),
                ('stirring_speed_coagulation_phase', models.IntegerField(default='', max_length=50)),
                ('duration_coagulation_phase', models.IntegerField(default='', max_length=50)),
                ('stirring_speed_flocculation_phase', models.IntegerField(default='', max_length=50)),
                ('duration_flocculation_phase', models.IntegerField(default='', max_length=50)),
                ('duration_sedimentation_phase', models.IntegerField(default='', max_length=50)),
            ],
        ),
    ]
