from pymodbus.client import ModbusTcpClient
from celery import shared_task
from django.apps import apps 
from datetime import datetime
import requests
import os
from .models import ComcenWeather, KalamtukanWeather, DanapaWeather
from django.utils.timezone import make_aware
from dotenv import load_dotenv


@shared_task
def store_modbus_data():
    Bywntest = apps.get_model('app1', 'Bywntest')
    Canalumtest = apps.get_model('app1', 'Canalumtest')
    Kalumbuyantest = apps.get_model('app1', 'Kalumbuyantest')
    Jugnotest = apps.get_model('app1', 'Jugnotest')

    modbus_devices = [
        {"ip": "192.168.41.10", "model": Bywntest},
        {"ip": "192.168.41.13", "model": Canalumtest},
        {"ip": "192.168.41.12", "model": Kalumbuyantest},
        {"ip": "192.168.41.18", "model": Jugnotest},
    ]

    results = {}

    for device in modbus_devices:
        client = ModbusTcpClient(device["ip"], port=100)
        data_value_cm = 0  # Default to 0 for any failure case

        try:
            if not client.connect():
                print(f"Could not connect to Modbus server at {device['ip']}, storing 0")
            else:
                result = client.read_holding_registers(address=6, count=1)
                if not result.isError() and result.registers is not None:
                    data_value_mm = result.registers[0]  # Data in millimeters
                    data_value_cm = data_value_mm / 10  # Convert mm to cm
                else:
                    print(f"No response from {device['ip']}, storing 0")

            # Save data to respective model
            device["model"].objects.create(data=data_value_cm)
            results[device["ip"]] = f"Data saved: {data_value_cm} cm"

        except Exception as e:
            print(f"Error with {device['ip']}: {e}")
            device["model"].objects.create(data=data_value_cm)  # Store 0 as set above
            results[device["ip"]] = f"Error, stored 0 in database: {e}"

        finally:
            client.close()

    return results


# Load environment variables from .env file
load_dotenv()

# Get API key and station IDs
API_KEY = os.getenv("WEATHER_API_KEY")
COMCEN_STATION_ID = "IBAYAW1"
KALAMTUKAN_STATION_ID = "IBAYAW2"
DANAPA_STATION_ID = "IBAYAW3"

# Move this function outside of the task so it can be used anywhere
def get_wind_direction(degrees):
    if degrees is None:
        return "N/A"
    directions = [
        "N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
        "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"
    ]
    index = int((degrees / 22.5) + 0.5) % 16
    return directions[index]


@shared_task
def fetch_and_store_comcen_weather():
    from .models import ComcenWeather
    api_url = f"https://www.wunderground.com/dashboard/pws/IBAYAW1"

    try:
        response = requests.get(api_url)
        
        # Check for 204 status code
        if response.status_code == 204:
            print("⚠️ Server Offline for COMCEN")
            # Save offline status to database
            timestamp = make_aware(datetime.now())
            ComcenWeather.objects.create(
                timestamp=timestamp,
                temperature="Server Offline",
                dewpoint="Server Offline",
                humidity="Server Offline",
                wind_direction="N/A",
                wind_speed="Server Offline",
                wind_gust="Server Offline",
                pressure="Server Offline",
                precip_rate="0.00 mm",
                precip_accum="0.00 mm",
            )
            print(f"✅ Server Offline status saved @ {timestamp}")
            return
            
        response.raise_for_status()
        data = response.json()
        if "observations" not in data:
            print("⚠️ No observation data")
            return

        obs = data["observations"][0]
        metric = obs.get("metric", {}) or {}

        # Convert obsTimeLocal to timezone-aware datetime
        obs_time = datetime.strptime(obs["obsTimeLocal"], "%Y-%m-%d %H:%M:%S")
        obs_time = make_aware(obs_time)

        # Check if data for this timestamp already exists
        if ComcenWeather.objects.filter(timestamp=obs_time).exists():
            print("✅ Skipped duplicate")
            return

        # Save to DB
        ComcenWeather.objects.create(
            timestamp=obs_time,
            temperature=f'{metric.get("temp", "N/A")} °C',
            dewpoint=f'{metric.get("dewpt", "N/A")} °C',
            humidity=f'{obs.get("humidity", "N/A")} %',
            wind_direction=get_wind_direction(obs.get("winddir")),
            wind_speed=f'{metric.get("windSpeed", "N/A")} km/h',
            wind_gust=f'{metric.get("windGust", "N/A")} km/h',
            pressure=f'{metric.get("pressure", "N/A")} hPa',
            precip_rate=f'{metric.get("precipRate", "0.00")} mm',
            precip_accum=f'{metric.get("precipTotal", "0.00")} mm',
        )
        print(f"✅ Weather data saved @ {obs_time}")

    except Exception as e:
        print("❌ Error fetching weather:", e)


@shared_task
def fetch_and_store_kalamtukan_weather():
    from .models import KalamtukanWeather
    api_url = f"https://api.weather.com/v2/pws/observations/current?stationId={KALAMTUKAN_STATION_ID}&format=json&units=m&apiKey={API_KEY}&numericPrecision=decimal"

    try:
        response = requests.get(api_url)
        
        # Check for 204 status code
        if response.status_code == 204:
            print("⚠️ Server Offline for KALAMTUKAN")
            # Save offline status to database
            timestamp = make_aware(datetime.now())
            KalamtukanWeather.objects.create(
                timestamp=timestamp,
                temperature="Server Offline",
                dewpoint="Server Offline",
                humidity="Server Offline",
                wind_direction="N/A",
                wind_speed="Server Offline",
                wind_gust="Server Offline",
                pressure="Server Offline",
                precip_rate="0.00 mm",
                precip_accum="0.00 mm",
            )
            print(f"✅ Server Offline status saved @ {timestamp}")
            return
            
        response.raise_for_status()
        data = response.json()
        if "observations" not in data:
            print("⚠️ No observation data")
            return

        obs = data["observations"][0]
        metric = obs.get("metric", {}) or {}

        # Convert obsTimeLocal to timezone-aware datetime
        obs_time = datetime.strptime(obs["obsTimeLocal"], "%Y-%m-%d %H:%M:%S")
        obs_time = make_aware(obs_time)

        # Check if data for this timestamp already exists
        if KalamtukanWeather.objects.filter(timestamp=obs_time).exists():
            print("✅ Skipped duplicate")
            return

        # Save to DB
        KalamtukanWeather.objects.create(
            timestamp=obs_time,
            temperature=f'{metric.get("temp", "N/A")} °C',
            dewpoint=f'{metric.get("dewpt", "N/A")} °C',
            humidity=f'{obs.get("humidity", "N/A")} %',
            wind_direction=get_wind_direction(obs.get("winddir")),
            wind_speed=f'{metric.get("windSpeed", "N/A")} km/h',
            wind_gust=f'{metric.get("windGust", "N/A")} km/h',
            pressure=f'{metric.get("pressure", "N/A")} hPa',
            precip_rate=f'{metric.get("precipRate", "0.00")} mm',
            precip_accum=f'{metric.get("precipTotal", "0.00")} mm',
        )
        print(f"✅ Weather data saved @ {obs_time}")

    except Exception as e:
        print("❌ Error fetching weather:", e)


@shared_task
def fetch_and_store_danapa_weather():
    from .models import DanapaWeather
    api_url = f"https://api.weather.com/v2/pws/observations/current?stationId={DANAPA_STATION_ID}&format=json&units=m&apiKey={API_KEY}&numericPrecision=decimal"

    try:
        response = requests.get(api_url)
        
        # Check for 204 status code
        if response.status_code == 204:
            print("⚠️ Server Offline for DANAPA")
            # Save offline status to database
            timestamp = make_aware(datetime.now())
            DanapaWeather.objects.create(
                timestamp=timestamp,
                temperature="Server Offline",
                dewpoint="Server Offline",
                humidity="Server Offline",
                wind_direction="N/A",
                wind_speed="Server Offline",
                wind_gust="Server Offline",
                pressure="Server Offline",
                precip_rate="0.00 mm",
                precip_accum="0.00 mm",
            )
            print(f"✅ Server Offline status saved @ {timestamp}")
            return
            
        response.raise_for_status()
        data = response.json()
        if "observations" not in data:
            print("⚠️ No observation data")
            return

        obs = data["observations"][0]
        metric = obs.get("metric", {}) or {}

        # Convert obsTimeLocal to timezone-aware datetime
        obs_time = datetime.strptime(obs["obsTimeLocal"], "%Y-%m-%d %H:%M:%S")
        obs_time = make_aware(obs_time)

        # Check if data for this timestamp already exists
        if DanapaWeather.objects.filter(timestamp=obs_time).exists():
            print("✅ Skipped duplicate")
            return

        # Save to DB
        DanapaWeather.objects.create(
            timestamp=obs_time,
            temperature=f'{metric.get("temp", "N/A")} °C',
            dewpoint=f'{metric.get("dewpt", "N/A")} °C',
            humidity=f'{obs.get("humidity", "N/A")} %',
            wind_direction=get_wind_direction(obs.get("winddir")),
            wind_speed=f'{metric.get("windSpeed", "N/A")} km/h',
            wind_gust=f'{metric.get("windGust", "N/A")} km/h',
            pressure=f'{metric.get("pressure", "N/A")} hPa',
            precip_rate=f'{metric.get("precipRate", "0.00")} mm',
            precip_accum=f'{metric.get("precipTotal", "0.00")} mm',
        )
        print(f"✅ Weather data saved @ {obs_time}")

    except Exception as e:
        print("❌ Error fetching weather:", e)


@shared_task
def fetch_all_weather_data():
    """
    Fetch and store weather data from all stations simultaneously
    This ensures all weather data is collected at the same time
    """
    try:
        # Use a common timestamp for all stations
        common_timestamp = make_aware(datetime.now())
        
        # Get API key and station IDs from environment variables
        api_key = API_KEY
        if not api_key:
            print("❌ API key not found in environment variables")
            return "Error: API key not found"
        
        # Get data from all stations at once
        stations = [
            {"id": COMCEN_STATION_ID, "model": ComcenWeather},
            {"id": KALAMTUKAN_STATION_ID, "model": KalamtukanWeather},
            {"id": DANAPA_STATION_ID, "model": DanapaWeather}
        ]
        
        for station in stations:
            api_url = f"https://api.weather.com/v2/pws/observations/current?stationId={station['id']}&format=json&units=m&apiKey={API_KEY}&numericPrecision=decimal"
            
            try:
                response = requests.get(api_url, timeout=10)
                
                # Check for 204 status code (No Content)
                if response.status_code == 204:
                    print(f"⚠️ Server Offline for station {station['id']}")
                    
                    # Save offline status to database
                    station["model"].objects.create(
                        timestamp=common_timestamp,
                        temperature="Server Offline",
                        dewpoint="Server Offline",
                        humidity="Server Offline",
                        wind_direction="N/A",
                        wind_speed="Server Offline",
                        wind_gust="Server Offline",
                        pressure="Server Offline",
                        precip_rate="0.00 mm",
                        precip_accum="0.00 mm",
                    )
                    print(f"✅ Server Offline status saved for {station['id']} @ {common_timestamp}")
                    continue
                
                response.raise_for_status()
                data = response.json()
                
                if "observations" not in data or not data["observations"]:
                    print(f"⚠️ No observation data for station {station['id']}")
                    continue
                
                obs = data["observations"][0]
                metric = obs.get("metric", {}) or {}
                
                # Use the API observation time but ensure timezone awareness
                obs_time = datetime.strptime(obs["obsTimeLocal"], "%Y-%m-%d %H:%M:%S")
                obs_time = make_aware(obs_time)
                
                # Save to DB - all stations will have data from the same timestamp period
                station["model"].objects.create(
                    timestamp=obs_time,
                    temperature=f'{metric.get("temp", "N/A")} °C',
                    dewpoint=f'{metric.get("dewpt", "N/A")} °C',
                    humidity=f'{obs.get("humidity", "N/A")} %',
                    wind_direction=get_wind_direction(obs.get("winddir")),
                    wind_speed=f'{metric.get("windSpeed", "N/A")} km/h',
                    wind_gust=f'{metric.get("windGust", "N/A")} km/h',
                    pressure=f'{metric.get("pressure", "N/A")} hPa',
                    precip_rate=f'{metric.get("precipRate", "0.00")} mm',
                    precip_accum=f'{metric.get("precipTotal", "0.00")} mm',
                )
                print(f"✅ Weather data saved for {station['id']} @ {obs_time}")
                
            except Exception as e:
                print(f"❌ Error fetching weather for {station['id']}: {e}")
        
        print("✅ All weather data fetched and stored simultaneously")
        return "All weather data fetch tasks completed"
        
    except Exception as e:
        print(f"❌ Error in fetch_all_weather_data: {e}")
        return f"Error: {e}"


@shared_task
def fetch_station_weather_data(station_id, model_class):
    """
    Fetch comprehensive weather data for a station
    """
    api_key = os.getenv("WEATHER_API_KEY")
    
    # Current conditions
    current_url = f"https://api.weather.com/v2/pws/observations/current?stationId={station_id}&format=json&units=m&apiKey={api_key}&numericPrecision=decimal"
    
    # Forecast data including astronomy
    forecast_url = f"https://api.weather.com/v2/pws/dailyforecast/7day?stationId={station_id}&format=json&units=m&apiKey={api_key}&numericPrecision=decimal"
    
    # Air quality data
    aqi_url = f"https://api.weather.com/v2/indices/pws/daily?stationId={station_id}&format=json&apiKey={api_key}"
    
    try:
        # Fetch current conditions
        current_response = requests.get(current_url)
        current_data = current_response.json()
        
        if current_response.status_code == 204:
            print(f"⚠️ Server Offline for station {station_id}")
            return
            
        obs = current_data["observations"][0]
        metric = obs.get("metric", {}) or {}
        
        # Fetch forecast and astronomy data
        forecast_response = requests.get(forecast_url)
        forecast_data = forecast_response.json()
        
        # Fetch air quality data
        aqi_response = requests.get(aqi_url)
        aqi_data = aqi_response.json()
        
        # Process and save data
        model_class.objects.create(
            timestamp=make_aware(datetime.strptime(obs["obsTimeLocal"], "%Y-%m-%d %H:%M:%S")),
            temperature=f'{metric.get("temp", "N/A")} °C',
            dewpoint=f'{metric.get("dewpt", "N/A")} °C',
            humidity=f'{obs.get("humidity", "N/A")} %',
            wind_direction=get_wind_direction(obs.get("winddir")),
            wind_speed=f'{metric.get("windSpeed", "N/A")} km/h',
            wind_gust=f'{metric.get("windGust", "N/A")} km/h',
            pressure=f'{metric.get("pressure", "N/A")} hPa',
            precip_rate=f'{metric.get("precipRate", "0.00")} mm',
            precip_accum=f'{metric.get("precipTotal", "0.00")} mm',
            
            # New fields
            feels_like=f'{metric.get("heatIndex", metric.get("temp", "N/A"))} °C',
            uv_index=forecast_data.get("uv", {}).get("index", 0),
            solar_radiation=obs.get("solarRadiation", 0.0),
            
            # Air Quality
            aqi=aqi_data.get("aqi", {}).get("value", 0),
            pm25=aqi_data.get("pm25", {}).get("value", 0.0),
            pm10=aqi_data.get("pm10", {}).get("value", 0.0),
            
            # Astronomy data
            sunrise=forecast_data.get("astronomy", {}).get("sunrise"),
            sunset=forecast_data.get("astronomy", {}).get("sunset"),
            moon_phase=forecast_data.get("astronomy", {}).get("moonPhase"),
            moon_illumination=forecast_data.get("astronomy", {}).get("moonIllumination", 0),
        )
        
    except Exception as e:
        print(f"❌ Error fetching weather for {station_id}: {e}")