# Generated by Django 5.1.6 on 2025-04-04 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bywntest',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField(auto_now_add=True)),
                ('time', models.TimeField(auto_now_add=True)),
                ('data', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Canalumtest',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField(auto_now_add=True)),
                ('time', models.TimeField(auto_now_add=True)),
                ('data', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='ComcenWeather',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
                ('temperature', models.CharField(max_length=10)),
                ('dewpoint', models.CharField(max_length=10)),
                ('humidity', models.CharField(max_length=10)),
                ('wind_direction', models.CharField(max_length=5)),
                ('wind_speed', models.CharField(max_length=10)),
                ('wind_gust', models.CharField(max_length=10)),
                ('pressure', models.CharField(max_length=10)),
                ('precip_rate', models.CharField(max_length=10)),
                ('precip_accum', models.CharField(max_length=10)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='DanapaWeather',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
                ('temperature', models.CharField(max_length=10)),
                ('dewpoint', models.CharField(max_length=10)),
                ('humidity', models.CharField(max_length=10)),
                ('wind_direction', models.CharField(max_length=5)),
                ('wind_speed', models.CharField(max_length=10)),
                ('wind_gust', models.CharField(max_length=10)),
                ('pressure', models.CharField(max_length=10)),
                ('precip_rate', models.CharField(max_length=10)),
                ('precip_accum', models.CharField(max_length=10)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='Jugnotest',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField(auto_now_add=True)),
                ('time', models.TimeField(auto_now_add=True)),
                ('data', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='KalamtukanWeather',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
                ('temperature', models.CharField(max_length=10)),
                ('dewpoint', models.CharField(max_length=10)),
                ('humidity', models.CharField(max_length=10)),
                ('wind_direction', models.CharField(max_length=5)),
                ('wind_speed', models.CharField(max_length=10)),
                ('wind_gust', models.CharField(max_length=10)),
                ('pressure', models.CharField(max_length=10)),
                ('precip_rate', models.CharField(max_length=10)),
                ('precip_accum', models.CharField(max_length=10)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='Kalumbuyantest',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField(auto_now_add=True)),
                ('time', models.TimeField(auto_now_add=True)),
                ('data', models.FloatField()),
            ],
        ),
    ]
