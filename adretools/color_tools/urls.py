from django.urls import path
from . import views

app_name = 'color_tools'

urlpatterns = [
    path('', views.color_home, name='home'),
    
    # SEO optimized URLs
    path('renk-secici/', views.color_home, name='color_picker_tr'),
    path('color-picker/', views.color_home, name='color_picker_en'),
    path('hex-renk-kodu/', views.color_home, name='hex_color_tr'),
    path('hex-color-code/', views.color_home, name='hex_color_en'),
    path('rgb-renk-donusturucu/', views.color_home, name='rgb_converter_tr'),
    path('rgb-color-converter/', views.color_home, name='rgb_converter_en'),
]