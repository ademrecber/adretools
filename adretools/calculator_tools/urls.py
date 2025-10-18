from django.urls import path
from . import views

app_name = 'calculator_tools'

urlpatterns = [
    path('', views.calculator_home, name='home'),
    
    # SEO optimized URLs
    path('bmi-calculator/', views.calculator_home, name='bmi_calculator'),
    path('body-mass-index-calculator/', views.calculator_home, name='bmi_calculator_seo'),
    path('vucut-kitle-indeksi-hesaplama/', views.calculator_home, name='bmi_calculator_tr'),
    
    path('age-calculator/', views.calculator_home, name='age_calculator'),
    path('calculate-age-from-birth-date/', views.calculator_home, name='age_calculator_seo'),
    path('yas-hesaplayici/', views.calculator_home, name='age_calculator_tr'),
    
    path('world-clock/', views.calculator_home, name='world_clock'),
    path('world-time-zones/', views.calculator_home, name='world_clock_seo'),
    path('dunya-saati/', views.calculator_home, name='world_clock_tr'),
    
    path('percentage-calculator/', views.calculator_home, name='percentage_calculator_en'),
    path('yuzde-hesaplayici/', views.calculator_home, name='percentage_calculator_tr'),
    path('date-calculator/', views.calculator_home, name='date_calculator_en'),
    path('tarih-hesaplayici/', views.calculator_home, name='date_calculator_tr'),
]