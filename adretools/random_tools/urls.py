from django.urls import path
from . import views

app_name = 'random_tools'

urlpatterns = [
    path('', views.random_home, name='home'),
    
    # SEO optimized URLs
    path('random-number-generator/', views.random_home, name='random_number_seo'),
    path('rastgele-sayi-uretici/', views.random_home, name='random_number_tr'),
    path('lucky-wheel-spinner/', views.random_home, name='lucky_wheel_seo'),
    path('sans-carki/', views.random_home, name='lucky_wheel_tr'),
    path('name-picker-lottery/', views.random_home, name='name_picker_seo'),
    path('kura-sistemi/', views.random_home, name='name_picker_tr'),
    path('dice-roller/', views.random_home, name='dice_roller_en'),
    path('zar-atma/', views.random_home, name='dice_roller_tr'),
    path('lottery-system/', views.random_home, name='lottery_system_en'),
    path('cekilis-sistemi/', views.random_home, name='lottery_system_tr'),
]