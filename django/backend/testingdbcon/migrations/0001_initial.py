# Generated by Django 4.1.3 on 2022-11-14 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='testuserdbcon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(default='', max_length=70)),
                ('Address', models.CharField(default='', max_length=200)),
                ('Date', models.DateField(default='')),
            ],
        ),
    ]
