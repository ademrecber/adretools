from django.urls import path
from . import views

urlpatterns = [
    path('', views.password_home, name='password_home'),
    path('generate/', views.generate_password, name='generate_password'),
    path('check/', views.check_password, name='check_password'),
    
    # SEO optimized URLs
    path('sifre-olusturucu/', views.password_home, name='password_generator_tr'),
    path('password-generator/', views.password_home, name='password_generator_en'),
    path('guclu-sifre-olustur/', views.password_home, name='strong_password_tr'),
    path('strong-password-generator/', views.password_home, name='strong_password_en'),
    path('sifre-kontrol/', views.password_home, name='password_checker_tr'),
    path('password-strength-checker/', views.password_home, name='password_checker_en'),
]