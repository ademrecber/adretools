from django.urls import path
from . import views

app_name = 'color_tools'

urlpatterns = [
    path('', views.color_home, name='home'),
    
    # English URLs (Primary)
    path('color-picker/', views.color_home, name='color_picker_en'),
    path('hex-color-code/', views.color_home, name='hex_color_en'),
    path('rgb-color-converter/', views.color_home, name='rgb_converter_en'),
]