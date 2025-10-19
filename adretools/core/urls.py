from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('terms-of-service/', views.terms_of_service, name='terms_of_service'),
    path('kullanim-sartlari/', views.terms_of_service, name='terms_of_service_tr'),
    path('cookie-policy/', views.cookie_policy, name='cookie_policy'),
    path('cerez-politikasi/', views.cookie_policy, name='cookie_policy_tr'),
]