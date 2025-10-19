from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('gizlilik-politikasi/', views.privacy_policy, name='privacy_policy_tr'),
]