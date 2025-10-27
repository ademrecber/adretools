from django.urls import path
from . import views

urlpatterns = [
    path('', views.card3d_home, name='card3d_home'),
    path('generate/', views.generate_3d_card, name='generate_3d_card'),
]