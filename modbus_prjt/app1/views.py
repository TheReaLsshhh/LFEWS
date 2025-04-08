import plotly.graph_objects as go
from plotly.offline import plot
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from app1.models import Bywntest, Canalumtest, Kalumbuyantest, Jugnotest
from datetime import datetime, timedelta
import pandas as pd
import xlsxwriter
import requests
import os
from .models import ComcenWeather, KalamtukanWeather, DanapaWeather
from django.utils.timezone import now

def dashboard_view(request):
    # Get selected date from request, default to today
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    current_date = datetime.now().date()
    current_time = datetime.now().time()

    if start_date and end_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        # Query data for date range
        bywntest_data = Bywntest.objects.filter(date__range=[start_date, end_date]).order_by('date', 'time')
        canalumtest_data = Canalumtest.objects.filter(date__range=[start_date, end_date]).order_by('date', 'time')
        kalumbuyantest_data = Kalumbuyantest.objects.filter(date__range=[start_date, end_date]).order_by('date', 'time')
        jugnotest_data = Jugnotest.objects.filter(date__range=[start_date, end_date]).order_by('date', 'time')
    else:
        # Get current date data including previous data points from today
        bywntest_data = Bywntest.objects.filter(date=current_date).order_by('date', 'time')
        canalumtest_data = Canalumtest.objects.filter(date=current_date).order_by('date', 'time')
        kalumbuyantest_data = Kalumbuyantest.objects.filter(date=current_date).order_by('date', 'time')
        jugnotest_data = Jugnotest.objects.filter(date=current_date).order_by('date', 'time')

    #Bayawan Data
    if not bywntest_data.exists():
        bywntest_dates = ["No Data"]
        bywntest_values = [0]
    else:
        bywntest_dates = []
        bywntest_values = []
        for data in bywntest_data:
            timestamp = f"{data.date} {data.time.strftime('%H:%M') if data.time else '00:00'}"
            if timestamp not in bywntest_dates:  # Avoid duplicate timestamps
                bywntest_dates.append(timestamp)
                bywntest_values.append(float(data.data))

    #Canalum Data  
    if not canalumtest_data.exists():
        canalumtest_dates = ["No Data"]
        canalumtest_values = [0]
    else:
        canalumtest_dates = []
        canalumtest_values = []
        for data in canalumtest_data:
            timestamp = f"{data.date} {data.time.strftime('%H:%M') if data.time else '00:00'}"
            if timestamp not in canalumtest_dates:
                canalumtest_dates.append(timestamp)
                canalumtest_values.append(float(data.data))

    #Kalumbuyan Data
    if not kalumbuyantest_data.exists():
        kalumbuyantest_dates = ["No Data"]
        kalumbuyantest_values = [0]
    else:
        kalumbuyantest_dates = []
        kalumbuyantest_values = []
        for data in kalumbuyantest_data:
            timestamp = f"{data.date} {data.time.strftime('%H:%M') if data.time else '00:00'}"
            if timestamp not in kalumbuyantest_dates:
                kalumbuyantest_dates.append(timestamp)
                kalumbuyantest_values.append(float(data.data))

    #Jugno Data
    if not jugnotest_data.exists():
        jugnotest_dates = ["No Data"]
        jugnotest_values = [0]
    else:
        jugnotest_dates = []
        jugnotest_values = []
        for data in jugnotest_data:
            timestamp = f"{data.date} {data.time.strftime('%H:%M') if data.time else '00:00'}"
            if timestamp not in jugnotest_dates:
                jugnotest_dates.append(timestamp)
                jugnotest_values.append(float(data.data))

    if request.GET.get('ajax') == '1':
        return JsonResponse({
            'bywntest': {'dates': bywntest_dates, 'values': bywntest_values},
            'canalumtest': {'dates': canalumtest_dates, 'values': canalumtest_values},
            'kalumbuyantest': {'dates': kalumbuyantest_dates, 'values': kalumbuyantest_values},
            'jugnotest': {'dates': jugnotest_dates, 'values': jugnotest_values}
        })

    bywntest_trace = go.Scatter(
        x=bywntest_dates, y=bywntest_values, mode='lines+markers',
        line=dict(color='#76e095', width=2),
        marker=dict(size=8, color='#76e095', symbol='circle'),
        name='Bywntest'
    )

    kalumbuyantest_trace = go.Scatter(
        x=kalumbuyantest_dates, y=kalumbuyantest_values, mode='lines+markers',
        line=dict(color='#76e095', width=2),
        marker=dict(size=8, color='#76e095', symbol='circle'),
        name='Kalumbuyantest'
    )

    jugnotest_trace = go.Scatter(
        x=jugnotest_dates, y=jugnotest_values, mode='lines+markers',
        line=dict(color='#76e095', width=2),
        marker=dict(size=8, color='#76e095', symbol='circle'),
        name='Jugnotest'
    )
    canalumtest_trace = go.Scatter(
        x=canalumtest_dates, y=canalumtest_values, mode='lines',
        line=dict(color='#e07695', width=2), fill='tozeroy',
        fillcolor='rgba(224, 118, 149, 0.1)', marker=dict(size=8, color='#e07695'),
        name='Canalumtest'
    )

    layout = go.Layout(
        paper_bgcolor='#141414', plot_bgcolor='#141414',
        xaxis=dict(title='Date and Time', tickfont=dict(color='white'), showgrid=False),
        yaxis=dict(title='Water Level (Meters)', tickfont=dict(color='white'), gridcolor='rgba(255,255,255,0.1)'),
        margin=dict(l=40, r=40, t=40, b=40), showlegend=True
    )

    fig = go.Figure(data=[bywntest_trace, canalumtest_trace, kalumbuyantest_trace, jugnotest_trace], layout=layout)
    plot_div = plot(fig, output_type='div')

    return render(request, 'dashboard.html', {'plot_div': plot_div})

def bayawan_view(request):
    return render(request, 'bayawan.html')

def canalum_view(request):
    return render(request, 'canalum.html')

def kalumbuyan_view(request):
    return render(request, 'kalumbuyan.html')

def jugno_view(request):
    return render(request, 'jugno.html')

def report_view(request):
    return render(request, 'report.html')

def export_excel(request):
    # Get date range from request
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    if not start_date or not end_date:
        return HttpResponse("Please provide both start and end dates", status=400)
    
    try:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    except ValueError:
        return HttpResponse("Invalid date format", status=400)
    
    # Query all data for the selected date range
    bayawan_data = Bywntest.objects.filter(date__range=[start_date, end_date]).order_by('date', 'time')
    canalum_data = Canalumtest.objects.filter(date__range=[start_date, end_date]).order_by('date', 'time')
    kalumbuyan_data = Kalumbuyantest.objects.filter(date__range=[start_date, end_date]).order_by('date', 'time')
    jugno_data = Jugnotest.objects.filter(date__range=[start_date, end_date]).order_by('date', 'time')
    
    # Create a response with Excel content type
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=water_level_data_{start_date}_to_{end_date}.xlsx'
    
    # Create Excel workbook and worksheet
    workbook = xlsxwriter.Workbook(response)
    worksheet = workbook.add_worksheet('Water Level Report')
    
    # Add styles
    header_format = workbook.add_format({
        'bold': True,
        'font_size': 12,
        'bg_color': '#333333',
        'font_color': 'white',
        'border': 1,
        'align': 'center',
        'valign': 'vcenter'
    })
    
    location_format = workbook.add_format({
        'bold': True,
        'font_size': 14,
        'bg_color': '#76e095',
        'font_color': 'black',
        'border': 1,
        'align': 'center',
        'valign': 'vcenter'
    })
    
    date_format = workbook.add_format({
        'num_format': 'yyyy-mm-dd',
        'border': 1
    })
    
    time_format = workbook.add_format({
        'num_format': 'hh:mm:ss',
        'border': 1
    })
    
    data_format = workbook.add_format({
        'border': 1,
        'num_format': '0.00'
    })
    
    # Add title and date range
    worksheet.merge_range('A1:D1', 'Water Level Report', header_format)
    worksheet.merge_range('A2:D2', f'Date Range: {start_date} to {end_date}', header_format)
    
    # Set column widths
    worksheet.set_column('A:A', 15)  # Date
    worksheet.set_column('B:B', 15)  # Time
    worksheet.set_column('C:C', 20)  # Water Level (cm)
    worksheet.set_column('D:D', 15)  # ID
    
    row = 3  # Starting row after title
    
    # Process each location
    for location_name, data_queryset in [
        ('Bayawan', bayawan_data),
        ('Canalum', canalum_data),
        ('Kalumbuyan', kalumbuyan_data),
        ('Jugno', jugno_data)
    ]:
        if not data_queryset.exists():
            continue
            
        # Add location header
        worksheet.merge_range(f'A{row}:D{row}', location_name, location_format)
        row += 1
        
        # Add column headers for this location
        worksheet.write(row, 0, 'Date', header_format)
        worksheet.write(row, 1, 'Time', header_format)
        worksheet.write(row, 2, 'Water Level (cm)', header_format)
        worksheet.write(row, 3, 'ID', header_format)
        row += 1
        
        # Add data for this location
        for item in data_queryset:
            worksheet.write_datetime(row, 0, item.date, date_format)
            worksheet.write_datetime(row, 1, item.time, time_format)
            worksheet.write_number(row, 2, float(item.data), data_format)
            worksheet.write_number(row, 3, item.id, data_format)
            row += 1
            
        # Add a blank row after each location for better readability
        row += 1
    
    workbook.close()
    return response


def weather_updates_view(request):
    return render(request, 'weather_updates.html')


API_KEY = os.getenv("WEATHER_API_KEY")

# Define the station details
STATIONS = [
    {"name": "Bayawan (UBOS)", "id": "IBAYAW1", "location": "Bayawan (Ubos)"},
    {"name": "Bayawan (KALAMTUKAN)", "id": "IBAYAW2", "location": "Bayawan (Kalamtukan)"},
    {"name": "Bayawan (DANAPA)", "id": "IBAYAW3", "location": "Bayawan (Kalumboyan)"},
]


# Convert wind direction degrees into cardinal directions
def get_wind_direction(degrees):
    if degrees is None:  # Ensure no error if winddir is missing
        return "N/A"

    directions = [
        "N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
        "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"
    ]
    index = int((degrees / 22.5) + 0.5) % 16
    return directions[index]


# Fetch weather data
def fetch_weather_data(station_id):
    # Use Weather Underground API URL format
    api_url = f"https://api.weather.com/v2/pws/observations/current?stationId={station_id}&format=json&units=m&apiKey={API_KEY}&numericPrecision=decimal"
    
    # Add required headers
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Accept': 'application/json'
    }

    try:
        # Add headers and proper timeout
        response = requests.get(api_url, headers=headers, timeout=10)
        
        # Check if response status is OK before parsing JSON
        if response.status_code != 200:
            # Special handling for 204 status code (No Content)
            if response.status_code == 204:
                return {
                    "error": "Server Offline",
                    "location": "N/A",
                    "temperature": "N/A",
                    "humidity": "N/A",
                    "wind_speed": "N/A",
                    "wind_gust": "N/A",
                    "wind_direction": "N/A",
                    "precip_rate": "N/A",
                    "precip_accum": "N/A",
                    "pressure": "N/A",
                    "dewpoint": "N/A",
                    "condition": "N/A",
                    "status": "Offline",
                    "updated_time": "N/A",
                }
            return {
                "error": f"API Error: Server returned status code {response.status_code}",
                "location": "N/A",
                "temperature": "N/A",
                "humidity": "N/A",
                "wind_speed": "N/A",
                "wind_gust": "N/A",
                "wind_direction": "N/A",
                "precip_rate": "N/A",
                "precip_accum": "N/A",
                "pressure": "N/A",
                "dewpoint": "N/A",
                "condition": "N/A",
                "status": "Offline",
                "updated_time": "N/A",
            }
        
        # Check if response content is not empty
        if not response.content:
            return {
                "error": "API Error: Empty response from server",
                "location": "N/A",
                "temperature": "N/A",
                "humidity": "N/A",
                "wind_speed": "N/A",
                "wind_gust": "N/A",
                "wind_direction": "N/A",
                "precip_rate": "N/A",
                "precip_accum": "N/A",
                "pressure": "N/A",
                "dewpoint": "N/A",
                "condition": "N/A",
                "status": "Offline",
                "updated_time": "N/A",
            }
        
        # Parse JSON response
        try:
            weather_data = response.json()
        except ValueError as e:
            print(f"JSON parsing error: {e}, Content: {response.content[:100]}")
            return {
                "error": f"API Error: Invalid JSON response",
                "location": "N/A",
                "temperature": "N/A",
                "humidity": "N/A",
                "wind_speed": "N/A",
                "wind_gust": "N/A",
                "wind_direction": "N/A",
                "precip_rate": "N/A",
                "precip_accum": "N/A",
                "pressure": "N/A",
                "dewpoint": "N/A",
                "condition": "N/A",
                "status": "Offline",
                "updated_time": "N/A",
            }

        if not weather_data or "observations" not in weather_data or not weather_data["observations"]:
            return {
                "error": "Invalid API response: No data received",
                "location": "N/A",
                "temperature": "N/A",
                "humidity": "N/A",
                "wind_speed": "N/A",
                "wind_gust": "N/A",
                "wind_direction": "N/A",
                "precip_rate": "N/A",
                "precip_accum": "N/A",
                "pressure": "N/A",
                "dewpoint": "N/A",
                "condition": "N/A",
                "status": "Offline",
                "updated_time": "N/A",
            }

        observation = weather_data["observations"][0]
        last_updated = observation.get("obsTimeLocal", "N/A")

        # Convert timestamp to "X minutes ago"
        if last_updated != "N/A":
            try:
                last_updated_time = datetime.strptime(last_updated, "%Y-%m-%d %H:%M:%S")
                time_difference = datetime.now() - last_updated_time
                minutes_ago = int(time_difference.total_seconds() // 60)
                status = f"Online (updated {minutes_ago} minutes ago)"
            except Exception as e:
                print(f"Error parsing timestamp: {e}")
                status = "Online (timestamp format error)"
        else:
            status = "Offline"

        # Get wind direction with error handling
        wind_dir_degrees = observation.get("winddir", None)
        wind_direction = get_wind_direction(wind_dir_degrees)
        
        # Safely get metric data with fallback
        metric_data = observation.get("metric", {}) or {}

        return {
            "temperature": metric_data.get("temp", "N/A"),
            "humidity": observation.get("humidity", "N/A"),
            "wind_speed": metric_data.get("windSpeed", "N/A"),
            "wind_gust": metric_data.get("windGust", "N/A"),
            "wind_direction": wind_direction,
            "precip_rate": metric_data.get("precipRate", "0.00"),
            "precip_accum": metric_data.get("precipTotal", "0.00"),
            "pressure": metric_data.get("pressure", "N/A"),
            "dewpoint": metric_data.get("dewpt", "N/A"),
            "condition": observation.get("wxPhraseLong", "N/A"),
            "status": status,
            "updated_time": last_updated,
        }
    except requests.exceptions.RequestException as e:
        print(f"Request error for station {station_id}: {str(e)}")
        return {
            "error": f"API Error: {str(e)}",
            "location": "N/A",
            "temperature": "N/A",
            "humidity": "N/A",
            "wind_speed": "N/A",
            "wind_gust": "N/A",
            "wind_direction": "N/A",
            "precip_rate": "N/A",
            "precip_accum": "N/A",
            "pressure": "N/A",
            "dewpoint": "N/A",
            "condition": "N/A",
            "status": "Offline",
            "updated_time": "N/A",
        }
    except Exception as e:
        print(f"Unexpected error for station {station_id}: {str(e)}")
        return {
            "error": f"Unexpected error: {str(e)}",
            "location": "N/A",
            "temperature": "N/A",
            "humidity": "N/A",
            "wind_speed": "N/A",
            "wind_gust": "N/A",
            "wind_direction": "N/A",
            "precip_rate": "N/A",
            "precip_accum": "N/A",
            "pressure": "N/A",
            "dewpoint": "N/A",
            "condition": "N/A",
            "status": "Offline",
            "updated_time": "N/A",
        }


# Main view
def weather_updates_view(request):
    weather_data = {}

    for station in STATIONS:
        weather_data[station["name"]] = fetch_weather_data(station["id"])

    return render(request, "weather_updates.html", {"weather_data": weather_data, "stations": STATIONS})

# Ensure this is at the top of views.py
API_KEY = os.getenv("WEATHER_API_KEY")  # Fetch API Key from environment
COMCEN_STATION_ID = "IBAYAW1", "IBAYAW2", "IBAYAW3"   # Ensure this is defined before usage

def fetch_comcen_weather_data():
    api_url = f"https://api.weather.com/v2/pws/observations/all/1day?stationId={COMCEN_STATION_ID}&format=json&units=m&apiKey={API_KEY}&numericPrecision=decimal"

    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()

        if "observations" not in data or not data["observations"]:
            return {"error": "No observations data available"}

        observations = data["observations"]

        weather_table_data = []
        for obs in observations:
            metric_data = obs.get("metric", {}) or {}
            time_str = obs.get("obsTimeLocal", "2000-01-01 00:00:00")
            time_formatted = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S").strftime("%I:%M %p")

            weather_table_data.append({
                "time": time_formatted,
                "temperature": f'{metric_data.get("temp", "N/A")} °C',
                "dewpoint": f'{metric_data.get("dewpt", "N/A")} °C',
                "humidity": f'{obs.get("humidity", "N/A")} %',
                "wind_direction": get_wind_direction(obs.get("winddir")),
                "wind_speed": f'{metric_data.get("windSpeed", "N/A")} km/h',
                "wind_gust": f'{metric_data.get("windGust", "N/A")} km/h',
                "pressure": f'{metric_data.get("pressure", "N/A")} hPa',
                "precip_rate": f'{metric_data.get("precipRate", "0.00")} mm',
                "precip_accum": f'{metric_data.get("precipTotal", "0.00")} mm',
            })

        return {"weather_table_data": weather_table_data[::-1]}  # Reverse for newest at top

    except requests.exceptions.RequestException as e:
        return {"error": f"API Error: {e}"}


def comcen_weather_view(request):
    # Get start_date and end_date from request parameters
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    
    now_time = now()
    
    # If no dates provided, default to showing today's data
    if not start_date:
        start_date = now_time.date().strftime('%Y-%m-%d')
    if not end_date:
        end_date = now_time.date().strftime('%Y-%m-%d')

    try:
        # Convert string dates to datetime objects
        start_datetime = datetime.strptime(start_date, '%Y-%m-%d').replace(hour=0, minute=0, second=0, microsecond=0)
        end_datetime = datetime.strptime(end_date, '%Y-%m-%d').replace(hour=23, minute=59, second=59, microsecond=999999)
        
        # Query records for the date range
        weather_records = ComcenWeather.objects.filter(
            timestamp__gte=start_datetime,
            timestamp__lte=end_datetime
        ).order_by("-timestamp")

        # Prepare data for the table
        weather_table_data = []
        for row in weather_records:
            weather_table_data.append({
                "time": row.timestamp.strftime("%Y-%m-%d %I:%M %p"),
                "temperature": row.temperature,
                "dewpoint": row.dewpoint,
                "humidity": row.humidity,
                "wind_direction": row.wind_direction,
                "wind_speed": row.wind_speed,
                "wind_gust": row.wind_gust,
                "pressure": row.pressure,
                "precip_rate": row.precip_rate,
                "precip_accum": row.precip_accum,
            })

    except ValueError:
        # Handle invalid date format
        weather_table_data = []

    return render(request, "comcen_weather.html", {
        "weather_data": {"weather_table_data": weather_table_data},
        "start_date": start_date,
        "end_date": end_date
    })

def kalamtukan_weather_view(request):
    # Get start_date and end_date from request parameters
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    
    now_time = now()
    
    # If no dates provided, default to showing today's data
    if not start_date:
        start_date = now_time.date().strftime('%Y-%m-%d')
    if not end_date:
        end_date = now_time.date().strftime('%Y-%m-%d')

    try:
        # Convert string dates to datetime objects
        start_datetime = datetime.strptime(start_date, '%Y-%m-%d').replace(hour=0, minute=0, second=0, microsecond=0)
        end_datetime = datetime.strptime(end_date, '%Y-%m-%d').replace(hour=23, minute=59, second=59, microsecond=999999)
        
        # Query records for the date range
        weather_records = KalamtukanWeather.objects.filter(
            timestamp__gte=start_datetime,
            timestamp__lte=end_datetime
        ).order_by("-timestamp")

        # Prepare data for the table
        weather_table_data = []
        for row in weather_records:
            weather_table_data.append({
                "time": row.timestamp.strftime("%Y-%m-%d %I:%M %p"),
                "temperature": row.temperature,
                "dewpoint": row.dewpoint,
                "humidity": row.humidity,
                "wind_direction": row.wind_direction,
                "wind_speed": row.wind_speed,
                "wind_gust": row.wind_gust,
                "pressure": row.pressure,
                "precip_rate": row.precip_rate,
                "precip_accum": row.precip_accum,
            })

    except ValueError:
        # Handle invalid date format
        weather_table_data = []

    return render(request, "kalamtukan_weather.html", {
        "weather_data": {"weather_table_data": weather_table_data},
        "start_date": start_date,
        "end_date": end_date
    })


def danapa_weather_view(request):
    # Get start_date and end_date from request parameters
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    
    now_time = now()
    
    # If no dates provided, default to showing today's data
    if not start_date:
        start_date = now_time.date().strftime('%Y-%m-%d')
    if not end_date:
        end_date = now_time.date().strftime('%Y-%m-%d')

    try:
        # Convert string dates to datetime objects
        start_datetime = datetime.strptime(start_date, '%Y-%m-%d').replace(hour=0, minute=0, second=0, microsecond=0)
        end_datetime = datetime.strptime(end_date, '%Y-%m-%d').replace(hour=23, minute=59, second=59, microsecond=999999)
        
        # Query records for the date range
        weather_records = DanapaWeather.objects.filter(
            timestamp__gte=start_datetime,
            timestamp__lte=end_datetime
        ).order_by("-timestamp")

        # Prepare data for the table
        weather_table_data = []
        for row in weather_records:
            weather_table_data.append({
                "time": row.timestamp.strftime("%Y-%m-%d %I:%M %p"),
                "temperature": row.temperature,
                "dewpoint": row.dewpoint,
                "humidity": row.humidity,
                "wind_direction": row.wind_direction,
                "wind_speed": row.wind_speed,
                "wind_gust": row.wind_gust,
                "pressure": row.pressure,
                "precip_rate": row.precip_rate,
                "precip_accum": row.precip_accum,
            })

    except ValueError:
        # Handle invalid date format
        weather_table_data = []

    return render(request, "danapa_weather.html", {
        "weather_data": {"weather_table_data": weather_table_data},
        "start_date": start_date,
        "end_date": end_date
    })

def map_view(request):
    return render(request, 'map.html')

def forecasting_view(request):
    """
    View for Weather Underground style forecasting page
    """
    API_KEY = os.getenv("WEATHER_API_KEY")
    if not API_KEY:
        return render(request, 'forecasting.html', {
            'error': 'Weather API key is not configured'
        })
    
    stations = {
        'IBAYAW1': {
            'name': 'Ubos Station',
            'elevation': '7 ft',
            'lat': '9.37',
            'lon': '122.81'
        },
        'IBAYAW2': {
            'name': 'Kalamtukan Station',
            'elevation': '5 ft',
            'lat': '9.37',
            'lon': '122.81'
        },
        'IBAYAW3': {
            'name': 'Danapa Station',
            'elevation': '325 ft',
            'lat': '9.37',
            'lon': '122.81'
        }
    }
    
    selected_station = request.GET.get('station', 'IBAYAW1')
    station_info = stations[selected_station]
    
    try:
        # Updated API endpoints for Weather Underground
        headers = {
            'User-Agent': 'Mozilla/5.0',
            'Accept': 'application/json'
        }
        
        # Current conditions endpoint
        current_url = (
            f"https://api.weather.com/v2/pws/observations/current"
            f"?stationId={selected_station}"
            f"&format=json"
            f"&units=m"
            f"&apiKey={API_KEY}"
            f"&numericPrecision=decimal"
        )
        
        print(f"Requesting URL: {current_url}")  # Debug log
        
        # Make request with proper headers and timeout
        current_response = requests.get(
            current_url,
            headers=headers,
            timeout=10
        )
        
        print(f"Response Status Code: {current_response.status_code}")  # Debug log
        print(f"Response Headers: {current_response.headers}")  # Debug log
        print(f"Response Content: {current_response.text[:200]}")  # Debug log
        
        if current_response.status_code == 204:
            return render(request, 'forecasting.html', {
                'error': f'No data available for station {selected_station}',
                'station_info': station_info,
                'stations': stations,
                'selected_station': selected_station
            })
            
        if current_response.status_code != 200:
            return render(request, 'forecasting.html', {
                'error': f'API returned status code {current_response.status_code}',
                'station_info': station_info,
                'stations': stations,
                'selected_station': selected_station
            })
            
        try:
            current_data = current_response.json()
        except ValueError as e:
            print(f"JSON Parse Error: {str(e)}")  # Debug log
            print(f"Response Content: {current_response.text}")  # Debug log
            return render(request, 'forecasting.html', {
                'error': f'Invalid data received from weather station {selected_station}',
                'station_info': station_info,
                'stations': stations,
                'selected_station': selected_station,
                'debug_info': {
                    'status_code': current_response.status_code,
                    'content_type': current_response.headers.get('content-type'),
                    'content': current_response.text[:200]
                }
            })
        
        if not current_data.get('observations'):
            return render(request, 'forecasting.html', {
                'error': f'No observations available for station {selected_station}',
                'station_info': station_info,
                'stations': stations,
                'selected_station': selected_station
            })
            
        # Process current conditions
        current = current_data['observations'][0]
        metric = current.get('metric', {})
        
        context = {
            'station_info': station_info,
            'stations': stations,
            'selected_station': selected_station,
            'current': {
                'temp': f"{metric.get('temp', 'N/A')}°C",
                'feels_like': f"{metric.get('heatIndex', metric.get('temp', 'N/A'))}°C",
                'humidity': f"{current.get('humidity', 'N/A')}%",
                'wind_speed': f"{metric.get('windSpeed', 0)} km/h",
                'wind_gust': f"{metric.get('windGust', 0)} km/h",
                'wind_dir': get_wind_direction(current.get('winddir')),
                'pressure': f"{metric.get('pressure', 'N/A')} hPa",
                'dew_point': f"{metric.get('dewpt', 'N/A')}°C",
                'precip_rate': f"{metric.get('precipRate', 0)} mm/hr",
                'precip_total': f"{metric.get('precipTotal', 0)} mm",
                'condition': current.get('condition', 'N/A'),
                'updated': current.get('obsTimeLocal', 'N/A')
            }
        }
        
        # Try to fetch forecast data
        try:
            forecast_url = (
                f"https://api.weather.com/v2/pws/dailyforecast/7day"
                f"?stationId={selected_station}"
                f"&format=json"
                f"&units=m"
                f"&apiKey={API_KEY}"
                f"&numericPrecision=decimal"
            )
            
            forecast_response = requests.get(forecast_url, headers=headers, timeout=10)
            if forecast_response.status_code == 200:
                forecast_data = forecast_response.json()
                context['forecast'] = forecast_data.get('forecast', [])
        except Exception as e:
            print(f"Forecast Error: {str(e)}")  # Debug log
            context['forecast'] = []
        
        return render(request, 'forecasting.html', context)
        
    except requests.RequestException as e:
        print(f"Request Error: {str(e)}")  # Debug log
        return render(request, 'forecasting.html', {
            'error': f'Error fetching weather data: {str(e)}',
            'station_info': station_info,
            'stations': stations,
            'selected_station': selected_station
        })
    except Exception as e:
        print(f"Unexpected Error: {str(e)}")  # Debug log
        return render(request, 'forecasting.html', {
            'error': f'An unexpected error occurred: {str(e)}',
            'station_info': station_info,
            'stations': stations,
            'selected_station': selected_station
        })

def map_data(request):
    # Fetch the latest water level data
    latest_bayawan = Bywntest.objects.order_by('-id').first()
    latest_canalum = Canalumtest.objects.order_by('-id').first()
    latest_kalumbuyan = Kalumbuyantest.objects.order_by('-id').first()
    latest_jugno = Jugnotest.objects.order_by('-id').first()
    
    # Fetch the latest weather data
    latest_comcen = ComcenWeather.objects.order_by('-timestamp').first()
    latest_kalamtukan = KalamtukanWeather.objects.order_by('-timestamp').first()
    latest_danapa = DanapaWeather.objects.order_by('-timestamp').first()
    
    # Define status based on water level
    def get_status(level):
        if level is None:
            return "Unknown"
        level_float = float(level)
        if level_float == 0:
            return "No Data"
        elif level_float < 1.0:
            return "Normal"
        elif level_float < 1.5:
            return "Moderate"
        elif level_float < 2.0:
            return "High"
        else:
            return "Critical"
    
    # Prepare data points for the map
    data_points = [
        # Water level sensors
        {
            'name': 'Bayawan Bridge Sensor',
            'lat': 9.368851,
            'lng': 122.801399,
            'type': 'water_level',
            'data': f"{float(latest_bayawan.data) if latest_bayawan else 0}m",
            'status': get_status(latest_bayawan.data if latest_bayawan else None),
            'last_updated': f"{latest_bayawan.date} {latest_bayawan.time.strftime('%H:%M:%S')}" if latest_bayawan else "N/A"
        },
        {
            'name': 'Canalum Creek Sensor',
            'lat': 9.3689,
            'lng': 122.7912,
            'type': 'water_level',
            'data': f"{float(latest_canalum.data) if latest_canalum else 0}m",
            'status': get_status(latest_canalum.data if latest_canalum else None),
            'last_updated': f"{latest_canalum.date} {latest_canalum.time.strftime('%H:%M:%S')}" if latest_canalum else "N/A"
        },
        {
            'name': 'Kalumbuyan Bridge Sensor',
            'lat': 9.4089,
            'lng': 122.8289,
            'type': 'water_level',
            'data': f"{float(latest_kalumbuyan.data) if latest_kalumbuyan else 0}m",
            'status': get_status(latest_kalumbuyan.data if latest_kalumbuyan else None),
            'last_updated': f"{latest_kalumbuyan.date} {latest_kalumbuyan.time.strftime('%H:%M:%S')}" if latest_kalumbuyan else "N/A"
        },
        {
            'name': 'Jugno Creek Sensor',
            'lat': 9.3831,
            'lng': 122.8152,
            'type': 'water_level',
            'data': f"{float(latest_jugno.data) if latest_jugno else 0}m",
            'status': get_status(latest_jugno.data if latest_jugno else None),
            'last_updated': f"{latest_jugno.date} {latest_jugno.time.strftime('%H:%M:%S')}" if latest_jugno else "N/A"
        },
        
        # Weather stations
        {
            'name': 'Ubos Weather Station',
            'lat': 9.368071364027939,
            'lng': 122.80823786739708,
            'type': 'weather',
            'temperature': latest_comcen.temperature if latest_comcen else "N/A",
            'humidity': latest_comcen.humidity if latest_comcen else "N/A",
            'wind_speed': latest_comcen.wind_speed if latest_comcen else "N/A",
            'wind_direction': latest_comcen.wind_direction if latest_comcen else "N/A",
            'precip_rate': latest_comcen.precip_rate if latest_comcen else "N/A",
            'pressure': latest_comcen.pressure if latest_comcen else "N/A",
            'last_updated': latest_comcen.timestamp.strftime("%Y-%m-%d %H:%M:%S") if latest_comcen else "N/A"
        },
        {
            'name': 'Kalamtukan Weather Station',
            'lat': 9.575943,
            'lng': 122.776005,
            'type': 'weather',
            'temperature': latest_kalamtukan.temperature if latest_kalamtukan else "N/A",
            'humidity': latest_kalamtukan.humidity if latest_kalamtukan else "N/A",
            'wind_speed': latest_kalamtukan.wind_speed if latest_kalamtukan else "N/A",
            'wind_direction': latest_kalamtukan.wind_direction if latest_kalamtukan else "N/A",
            'precip_rate': latest_kalamtukan.precip_rate if latest_kalamtukan else "N/A",
            'pressure': latest_kalamtukan.pressure if latest_kalamtukan else "N/A",
            'last_updated': latest_kalamtukan.timestamp.strftime("%Y-%m-%d %H:%M:%S") if latest_kalamtukan else "N/A"
        },
        {
            'name': 'Danapa Weather Station',
            'lat': 9.472166,
            'lng': 122.817721,
            'type': 'weather',
            'temperature': latest_danapa.temperature if latest_danapa else "N/A",
            'humidity': latest_danapa.humidity if latest_danapa else "N/A",
            'wind_speed': latest_danapa.wind_speed if latest_danapa else "N/A",
            'wind_direction': latest_danapa.wind_direction if latest_danapa else "N/A",
            'precip_rate': latest_danapa.precip_rate if latest_danapa else "N/A",
            'pressure': latest_danapa.pressure if latest_danapa else "N/A",
            'last_updated': latest_danapa.timestamp.strftime("%Y-%m-%d %H:%M:%S") if latest_danapa else "N/A"
        }
    ]
    
    return JsonResponse({'data_points': data_points})

def weather_api(request, station_id):
    """API endpoint for real-time weather updates"""
    API_KEY = os.getenv("WEATHER_API_KEY")
    
    try:
        # Current conditions endpoint
        headers = {
            'User-Agent': 'Mozilla/5.0',
            'Accept': 'application/json'
        }
        
        current_url = (
            f"https://api.weather.com/v2/pws/observations/current"
            f"?stationId={station_id}"
            f"&format=json"
            f"&units=m"
            f"&apiKey={API_KEY}"
            f"&numericPrecision=decimal"
        )
        
        current_response = requests.get(current_url, headers=headers, timeout=10)
        
        if current_response.status_code != 200:
            return JsonResponse({'error': f'API returned status code {current_response.status_code}'}, status=500)
            
        current_data = current_response.json()
        
        if not current_data.get('observations'):
            return JsonResponse({'error': 'No observations available'}, status=404)
            
        current = current_data['observations'][0]
        metric = current.get('metric', {})
        
        return JsonResponse({
            'temp': f"{metric.get('temp', 'N/A')}°C",
            'feels_like': f"{metric.get('heatIndex', metric.get('temp', 'N/A'))}°C",
            'humidity': f"{current.get('humidity', 'N/A')}%",
            'wind_speed': f"{metric.get('windSpeed', 0)} km/h",
            'wind_dir': get_wind_direction(current.get('winddir')),
            'pressure': f"{metric.get('pressure', 'N/A')} hPa",
            'dew_point': f"{metric.get('dewpt', 'N/A')}°C",
            'precip_rate': f"{metric.get('precipRate', 0)} mm/hr",
            'precip_total': f"{metric.get('precipTotal', 0)} mm",
            'condition': current.get('condition', 'N/A'),
            'updated': current.get('obsTimeLocal', 'N/A')
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)