from django.urls import path
from . import views

app_name = 'password_tools'

urlpatterns = [
    path('', views.password_home, name='home'),
    path('generate/', views.generate_password, name='generate_password'),
    path('check/', views.check_password, name='check_password'),
    
    # English URLs (Primary)
    path('password-generator/', views.password_home, name='password_generator_en'),
    path('strong-password-generator/', views.password_home, name='strong_password_en'),
    path('password-strength-checker/', views.password_home, name='password_checker_en'),
]