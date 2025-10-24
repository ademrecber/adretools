from django.urls import path
from . import views

app_name = 'calculator_tools'

urlpatterns = [
    path('', views.calculator_home, name='home'),
    
    # English URLs (Primary)
    path('bmi-calculator/', views.calculator_home, name='bmi_calculator'),
    path('body-mass-index-calculator/', views.calculator_home, name='bmi_calculator_seo'),
    path('age-calculator/', views.calculator_home, name='age_calculator'),
    path('calculate-age-from-birth-date/', views.calculator_home, name='age_calculator_seo'),
    path('world-clock/', views.calculator_home, name='world_clock'),
    path('world-time-zones/', views.calculator_home, name='world_clock_seo'),
    path('percentage-calculator/', views.calculator_home, name='percentage_calculator_en'),
    path('date-calculator/', views.calculator_home, name='date_calculator_en'),
]