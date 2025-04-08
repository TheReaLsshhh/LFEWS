from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('bayawan/', views.bayawan_view, name='bayawan_view'),
    path('canalum/', views.canalum_view, name='canalum_view'),
    path('kalumbuyan/', views.kalumbuyan_view, name='kalumbuyan_view'),
    path('jugno/', views.jugno_view, name='jugno_view'),
    path('report/', views.report_view, name='report_view'),
    path('export-excel/', views.export_excel, name='export_excel'),
    path('comcen-weather/', views.comcen_weather_view, name='comcen_weather'),
    path('weather-updates/', views.weather_updates_view, name='weather_updates_view'),
    path('kalamtukan-weather/', views.kalamtukan_weather_view, name='kalamtukan_weather'),
    path('danapa-weather/', views.danapa_weather_view, name='danapa_weather'),
    path('', views.map_view, name='map_view'),
    path('map-data/', views.map_data, name='map_data'),
    path('forecasting/', views.forecasting_view, name='forecasting_view'),
]
