from django.urls import path
from . import views

app_name = 'random_tools'

urlpatterns = [
    path('', views.random_home, name='home'),
    
    # English URLs (Primary)
    path('random-number-generator/', views.random_home, name='random_number_seo'),
    path('lucky-wheel-spinner/', views.random_home, name='lucky_wheel_seo'),
    path('name-picker-lottery/', views.random_home, name='name_picker_seo'),
    path('dice-roller/', views.random_home, name='dice_roller_en'),
    path('lottery-system/', views.random_home, name='lottery_system_en'),
]