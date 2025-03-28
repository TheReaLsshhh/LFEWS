from django.contrib import admin
from django.urls import path
from . import views
from .views import dashboard_view


urlpatterns = [
    path('', dashboard_view, name='dashboard'),
    path('bayawan/', views.bayawan_view, name='bayawan_view'),
    path('canalum/', views.canalum_view, name='canalum_view'),
    path('kalumbuyan/', views.kalumbuyan_view, name='kalumbuyan_view'),
    path('jugno/', views.jugno_view, name='jugno_view'),
    path('report/', views.report_view, name='report_view'),
    path('export-excel/', views.export_excel, name='export_excel'),
]
