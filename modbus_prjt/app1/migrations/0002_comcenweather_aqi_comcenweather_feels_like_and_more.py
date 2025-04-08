# Generated by Django 5.1.6 on 2025-04-06 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comcenweather',
            name='aqi',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='comcenweather',
            name='feels_like',
            field=models.CharField(default='N/A', max_length=10),
        ),
        migrations.AddField(
            model_name='comcenweather',
            name='grass_pollen',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='comcenweather',
            name='moon_illumination',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='comcenweather',
            name='moon_phase',
            field=models.CharField(default='N/A', max_length=20),
        ),
        migrations.AddField(
            model_name='comcenweather',
            name='pm10',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='comcenweather',
            name='pm25',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='comcenweather',
            name='solar_radiation',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='comcenweather',
            name='sunrise',
            field=models.TimeField(null=True),
        ),
        migrations.AddField(
            model_name='comcenweather',
            name='sunset',
            field=models.TimeField(null=True),
        ),
        migrations.AddField(
            model_name='comcenweather',
            name='tree_pollen',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='comcenweather',
            name='uv_index',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='comcenweather',
            name='weed_pollen',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='danapaweather',
            name='aqi',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='danapaweather',
            name='feels_like',
            field=models.CharField(default='N/A', max_length=10),
        ),
        migrations.AddField(
            model_name='danapaweather',
            name='grass_pollen',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='danapaweather',
            name='moon_illumination',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='danapaweather',
            name='moon_phase',
            field=models.CharField(default='N/A', max_length=20),
        ),
        migrations.AddField(
            model_name='danapaweather',
            name='pm10',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='danapaweather',
            name='pm25',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='danapaweather',
            name='solar_radiation',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='danapaweather',
            name='sunrise',
            field=models.TimeField(null=True),
        ),
        migrations.AddField(
            model_name='danapaweather',
            name='sunset',
            field=models.TimeField(null=True),
        ),
        migrations.AddField(
            model_name='danapaweather',
            name='tree_pollen',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='danapaweather',
            name='uv_index',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='danapaweather',
            name='weed_pollen',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='kalamtukanweather',
            name='aqi',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='kalamtukanweather',
            name='feels_like',
            field=models.CharField(default='N/A', max_length=10),
        ),
        migrations.AddField(
            model_name='kalamtukanweather',
            name='grass_pollen',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='kalamtukanweather',
            name='moon_illumination',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='kalamtukanweather',
            name='moon_phase',
            field=models.CharField(default='N/A', max_length=20),
        ),
        migrations.AddField(
            model_name='kalamtukanweather',
            name='pm10',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='kalamtukanweather',
            name='pm25',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='kalamtukanweather',
            name='solar_radiation',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='kalamtukanweather',
            name='sunrise',
            field=models.TimeField(null=True),
        ),
        migrations.AddField(
            model_name='kalamtukanweather',
            name='sunset',
            field=models.TimeField(null=True),
        ),
        migrations.AddField(
            model_name='kalamtukanweather',
            name='tree_pollen',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='kalamtukanweather',
            name='uv_index',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='kalamtukanweather',
            name='weed_pollen',
            field=models.IntegerField(default=0),
        ),
    ]
