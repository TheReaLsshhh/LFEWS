import plotly.graph_objects as go
from plotly.offline import plot
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from app1.models import Bywntest, Canalumtest, Kalumbuyantest, Jugnotest
from datetime import datetime, timedelta
import pandas as pd
import xlsxwriter

def dashboard_view(request):
    # Get selected date from request, default to today
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date and end_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        # Query data for date range
        bywntest_data = Bywntest.objects.filter(date__range=[start_date, end_date]).order_by('date', 'time')
        canalumtest_data = Canalumtest.objects.filter(date__range=[start_date, end_date]).order_by('date', 'time')
        kalumbuyantest_data = Kalumbuyantest.objects.filter(date__range=[start_date, end_date]).order_by('date', 'time')
        jugnotest_data = Jugnotest.objects.filter(date__range=[start_date, end_date]).order_by('date', 'time')
    else:
        # Get current date data
        current_date = datetime.now().date()
        bywntest_data = Bywntest.objects.filter(date=current_date).order_by('time')
        canalumtest_data = Canalumtest.objects.filter(date=current_date).order_by('time')
        kalumbuyantest_data = Kalumbuyantest.objects.filter(date=current_date).order_by('time')
        jugnotest_data = Jugnotest.objects.filter(date=current_date).order_by('time')
    #Bayawan Data
    if not bywntest_data.exists():
        bywntest_dates = ["No Data"]
        bywntest_values = [0]
    else:
        bywntest_dates = [
            f"{data.date} {data.time.strftime('%H:%M') if data.time else '00:00'}"
            for data in bywntest_data
        ]
        bywntest_values = [float(data.data) for data in bywntest_data]
    #Canalum Data
    if not canalumtest_data.exists():
        canalumtest_dates = ["No Data"]
        canalumtest_values = [0]
    else:
        canalumtest_dates = [
            f"{data.date} {data.time.strftime('%H:%M') if data.time else '00:00'}"
            for data in canalumtest_data
        ]
        canalumtest_values = [float(data.data) for data in canalumtest_data]
    #Kalumbuyan Data
    if not kalumbuyantest_data.exists():
        kalumbuyantest_dates = ["No Data"]
        kalumbuyantest_values = [0]
    else:
        kalumbuyantest_dates = [
            f"{data.date} {data.time.strftime('%H:%M') if data.time else '00:00'}"
            for data in kalumbuyantest_data
        ]
        kalumbuyantest_values = [float(data.data) for data in kalumbuyantest_data]
    #Jugno Data
    if not jugnotest_data.exists():
        jugnotest_dates = ["No Data"]
        jugnotest_values = [0]
    else:
        jugnotest_dates = [
            f"{data.date} {data.time.strftime('%H:%M') if data.time else '00:00'}"
            for data in jugnotest_data
        ]
        jugnotest_values = [float(data.data) for data in jugnotest_data]

    if request.GET.get('ajax') == '1':
        return JsonResponse({
            'bywntest': {'dates': bywntest_dates, 'values': bywntest_values},
            'canalumtest': {'dates': canalumtest_dates, 'values': canalumtest_values},
            'kalumbuyantest': {'dates': kalumbuyantest_dates, 'values': kalumbuyantest_values},
            'jugnotest': {'dates': jugnotest_dates, 'values': jugnotest_values}
        })

    bywntest_trace = go.Scatter(
        x=bywntest_dates, y=bywntest_values, mode='lines',
        line=dict(color='#76e095', width=2), fill='tozeroy',
        fillcolor='rgba(118, 224, 149, 0.1)', marker=dict(size=8, color='#76e095'),
        name='Bywntest'
    )

    kalumbuyantest_trace = go.Scatter(
        x=kalumbuyantest_dates, y=kalumbuyantest_values, mode='lines',
        line=dict(color='#76e095', width=2), fill='tozeroy',
        fillcolor='rgba(118, 224, 149, 0.1)', marker=dict(size=8, color='#76e095'),
        name='Kalumbuyantest'
    )

    jugnotest_trace = go.Scatter(
        x=jugnotest_dates, y=jugnotest_values, mode='lines',
        line=dict(color='#76e095', width=2), fill='tozeroy',
        fillcolor='rgba(118, 224, 149, 0.1)', marker=dict(size=8, color='#76e095'),
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