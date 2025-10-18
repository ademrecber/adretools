from django.urls import path
from . import views

app_name = 'horoscope_tools'

urlpatterns = [
    path('', views.horoscope_home, name='home'),
    path('calculate/', views.calculate_horoscope, name='calculate_horoscope'),
    
    # SEO optimized URLs
    path('burc-hesaplama/', views.horoscope_home, name='horoscope_calculator_tr'),
    path('horoscope-calculator/', views.horoscope_home, name='horoscope_calculator_en'),
    path('dogum-tarihi-burc/', views.horoscope_home, name='birth_date_horoscope_tr'),
    path('birth-date-horoscope/', views.horoscope_home, name='birth_date_horoscope_en'),
    path('burc-ozellikleri/', views.horoscope_home, name='zodiac_traits_tr'),
    path('zodiac-sign-traits/', views.horoscope_home, name='zodiac_traits_en'),
    path('astroloji-hesaplama/', views.horoscope_home, name='astrology_calculator_tr'),
    path('astrology-calculator/', views.horoscope_home, name='astrology_calculator_en'),
]