# Generated by Django 4.1.3 on 2023-02-28 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db_connection', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='bsf_data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('diameter', models.IntegerField(default='')),
                ('material', models.CharField(default='', max_length=50)),
                ('material_height', models.FloatField(default='')),
                ('min_grain_diameter', models.FloatField(default='')),
                ('max_grain_diameter', models.FloatField(default='')),
                ('mean_grain_diameter', models.FloatField(default='')),
                ('min_flow', models.FloatField(default='')),
                ('max_flow', models.FloatField(default='')),
                ('mean_flow', models.FloatField(default='')),
                ('min_pause', models.IntegerField(default='')),
                ('max_pause', models.IntegerField(default='')),
                ('mean_pause', models.IntegerField(default='')),
                ('time_schmutzdecke', models.IntegerField(default='')),
                ('initial_ecoli', models.FloatField(default='')),
                ('final_ecoli', models.FloatField(default='')),
                ('initial_turbidity', models.IntegerField(default='')),
                ('final_turbidity', models.IntegerField(default='')),
            ],
        ),
        migrations.AlterField(
            model_name='flocculation_data',
            name='cal_final_EC',
            field=models.FloatField(default=''),
        ),
        migrations.AlterField(
            model_name='flocculation_data',
            name='delta_EC',
            field=models.FloatField(default=''),
        ),
        migrations.AlterField(
            model_name='flocculation_data',
            name='duration_coagulation_phase',
            field=models.IntegerField(default=''),
        ),
        migrations.AlterField(
            model_name='flocculation_data',
            name='duration_flocculation_phase',
            field=models.IntegerField(default=''),
        ),
        migrations.AlterField(
            model_name='flocculation_data',
            name='duration_sedimentation_phase',
            field=models.IntegerField(default=''),
        ),
        migrations.AlterField(
            model_name='flocculation_data',
            name='final_EC',
            field=models.IntegerField(default=''),
        ),
        migrations.AlterField(
            model_name='flocculation_data',
            name='final_pH',
            field=models.FloatField(default=''),
        ),
        migrations.AlterField(
            model_name='flocculation_data',
            name='final_turbidity',
            field=models.IntegerField(default=''),
        ),
        migrations.AlterField(
            model_name='flocculation_data',
            name='floc_cactus_share',
            field=models.FloatField(default=''),
        ),
        migrations.AlterField(
            model_name='flocculation_data',
            name='floc_concentration',
            field=models.FloatField(default=''),
        ),
        migrations.AlterField(
            model_name='flocculation_data',
            name='floc_dose',
            field=models.IntegerField(default=''),
        ),
        migrations.AlterField(
            model_name='flocculation_data',
            name='floc_saline_Molarity',
            field=models.FloatField(default=''),
        ),
        migrations.AlterField(
            model_name='flocculation_data',
            name='floc_vol',
            field=models.FloatField(default=''),
        ),
        migrations.AlterField(
            model_name='flocculation_data',
            name='initial_EC',
            field=models.IntegerField(default=''),
        ),
        migrations.AlterField(
            model_name='flocculation_data',
            name='initial_pH',
            field=models.FloatField(default=''),
        ),
        migrations.AlterField(
            model_name='flocculation_data',
            name='initial_turbidity',
            field=models.IntegerField(default=''),
        ),
        migrations.AlterField(
            model_name='flocculation_data',
            name='saline_concentration',
            field=models.FloatField(default=''),
        ),
        migrations.AlterField(
            model_name='flocculation_data',
            name='stirring_speed_coagulation_phase',
            field=models.IntegerField(default=''),
        ),
        migrations.AlterField(
            model_name='flocculation_data',
            name='stirring_speed_flocculation_phase',
            field=models.IntegerField(default=''),
        ),
    ]
