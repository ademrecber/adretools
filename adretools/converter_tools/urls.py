from django.urls import path
from . import views

app_name = 'converter_tools'

urlpatterns = [
    path('', views.converter_home, name='converter_home'),
    path('convert/', views.convert_unit, name='convert_unit'),
    
    # English URLs (Primary)
    path('unit-converter/', views.converter_home, name='unit_converter_en'),
    path('length-converter/', views.converter_home, name='length_converter_en'),
    path('weight-converter/', views.converter_home, name='weight_converter_en'),
    path('temperature-converter/', views.converter_home, name='temperature_converter_en'),
]