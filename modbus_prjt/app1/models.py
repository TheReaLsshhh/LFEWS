from django.db import models

class Kalumbuyantest(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    data = models.FloatField()  # Stores water level in centimeters

    def __str__(self):
        return f"{self.date} {self.time} - {self.data} cm"


class Canalumtest(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    data = models.FloatField()  # Stores water level in centimeters

    def __str__(self):
        return f"{self.date} {self.time} - {self.data} cm"
    

class Bywntest(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    data = models.FloatField()  # Stores water level in centimeters

    def __str__(self):
        return f"{self.date} {self.time} - {self.data} cm"
    

class Jugnotest(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    data = models.FloatField()  # Stores water level in centimeters

    def __str__(self):
        return f"{self.date} {self.time} - {self.data} cm"
    

class WeatherStationBase(models.Model):
    timestamp = models.DateTimeField()
    temperature = models.CharField(max_length=10)
    dewpoint = models.CharField(max_length=10)
    humidity = models.CharField(max_length=10)
    wind_direction = models.CharField(max_length=5)
    wind_speed = models.CharField(max_length=10)
    wind_gust = models.CharField(max_length=10)
    pressure = models.CharField(max_length=10)
    precip_rate = models.CharField(max_length=10)
    precip_accum = models.CharField(max_length=10)
    
    # New fields for Weather Underground style
    feels_like = models.CharField(max_length=10, default='N/A')
    uv_index = models.IntegerField(default=0)
    solar_radiation = models.FloatField(default=0.0)
    
    # Air Quality
    aqi = models.IntegerField(default=0)
    pm25 = models.FloatField(default=0.0)
    pm10 = models.FloatField(default=0.0)
    
    # Pollen
    tree_pollen = models.IntegerField(default=0)
    grass_pollen = models.IntegerField(default=0)
    weed_pollen = models.IntegerField(default=0)
    
    # Astronomy
    sunrise = models.TimeField(null=True)
    sunset = models.TimeField(null=True)
    moon_phase = models.CharField(max_length=20, default='N/A')
    moon_illumination = models.IntegerField(default=0)

    class Meta:
        abstract = True
        ordering = ['-timestamp']

class ComcenWeather(WeatherStationBase):
    def __str__(self):
        return f"COMCEN Weather @ {self.timestamp}"

class KalamtukanWeather(WeatherStationBase):
    def __str__(self):
        return f"Kalamtukan Weather @ {self.timestamp}"

class DanapaWeather(WeatherStationBase):
    def __str__(self):
        return f"Danapa Weather @ {self.timestamp}"
