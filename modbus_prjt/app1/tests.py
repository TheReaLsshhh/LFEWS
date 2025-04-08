from django.test import TestCase, Client
from django.urls import reverse
from .models import Bywntest, Canalumtest, Kalumbuyantest, Jugnotest, ComcenWeather, KalamtukanWeather, DanapaWeather
from django.utils import timezone
import json
from datetime import datetime


class MapDataTests(TestCase):
    def setUp(self):
        # Create test data for water level and weather models
        test_date = timezone.now().date()
        test_time = timezone.now().time()
        
        # Water level test data
        Bywntest.objects.create(data=1.2, date=test_date, time=test_time)
        Canalumtest.objects.create(data=0.8, date=test_date, time=test_time)
        Kalumbuyantest.objects.create(data=1.5, date=test_date, time=test_time)
        Jugnotest.objects.create(data=2.1, date=test_date, time=test_time)
        
        # Weather test data
        timestamp = timezone.now()
        ComcenWeather.objects.create(
            timestamp=timestamp,
            temperature="30.5 °C",
            dewpoint="25.3 °C",
            humidity="75 %",
            wind_direction="NW",
            wind_speed="10 km/h",
            wind_gust="15 km/h",
            pressure="1012 hPa",
            precip_rate="0.00 mm",
            precip_accum="0.00 mm"
        )
        
        KalamtukanWeather.objects.create(
            timestamp=timestamp,
            temperature="29.8 °C",
            dewpoint="24.5 °C",
            humidity="78 %",
            wind_direction="W",
            wind_speed="12 km/h",
            wind_gust="18 km/h",
            pressure="1013 hPa",
            precip_rate="0.50 mm",
            precip_accum="2.00 mm"
        )
        
        DanapaWeather.objects.create(
            timestamp=timestamp,
            temperature="31.2 °C",
            dewpoint="26.0 °C",
            humidity="72 %",
            wind_direction="SE",
            wind_speed="8 km/h",
            wind_gust="14 km/h",
            pressure="1010 hPa",
            precip_rate="0.00 mm",
            precip_accum="0.00 mm"
        )
        
    def test_map_data_api(self):
        """Test that the map data API returns data in the expected format"""
        client = Client()
        response = client.get(reverse('map_data'))
        
        # Check response status code
        self.assertEqual(response.status_code, 200)
        
        # Parse the JSON response
        data = json.loads(response.content)
        
        # Check that the data contains data_points
        self.assertIn('data_points', data)
        
        # Check we have the expected number of data points (7 total)
        self.assertEqual(len(data['data_points']), 7)
        
        # Check content of a water level sensor
        bayawan_sensor = next((item for item in data['data_points'] if item['name'] == 'Bayawan Bridge Sensor'), None)
        self.assertIsNotNone(bayawan_sensor)
        self.assertEqual(bayawan_sensor['type'], 'water_level')
        self.assertEqual(bayawan_sensor['data'], '1.2m')
        self.assertEqual(bayawan_sensor['status'], 'Moderate')
        
        # Check content of a weather station
        comcen_station = next((item for item in data['data_points'] if item['name'] == 'Comcen Weather Station'), None)
        self.assertIsNotNone(comcen_station)
        self.assertEqual(comcen_station['type'], 'weather')
        self.assertEqual(comcen_station['temperature'], '30.5 °C')
        self.assertEqual(comcen_station['humidity'], '75 %')
        
        # Check Jugno sensor has critical status (>2.0m)
        jugno_sensor = next((item for item in data['data_points'] if item['name'] == 'Jugno Creek Sensor'), None)
        self.assertIsNotNone(jugno_sensor)
        self.assertEqual(jugno_sensor['status'], 'Critical')


