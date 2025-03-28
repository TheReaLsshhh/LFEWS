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