from django.urls import path
from . import views

urlpatterns = [
    path('', views.converter_home, name='converter_home'),
    path('convert/', views.convert_unit, name='convert_unit'),
    
    # SEO optimized URLs
    path('birim-donusturucu/', views.converter_home, name='unit_converter_tr'),
    path('unit-converter/', views.converter_home, name='unit_converter_en'),
    path('uzunluk-donusturucu/', views.converter_home, name='length_converter_tr'),
    path('length-converter/', views.converter_home, name='length_converter_en'),
    path('agirlik-donusturucu/', views.converter_home, name='weight_converter_tr'),
    path('weight-converter/', views.converter_home, name='weight_converter_en'),
    path('sicaklik-donusturucu/', views.converter_home, name='temperature_converter_tr'),
    path('temperature-converter/', views.converter_home, name='temperature_converter_en'),
]