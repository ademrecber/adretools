from django.urls import path
from . import views

app_name = 'ai_tools'

urlpatterns = [
    path('', views.ai_home, name='home'),
    path('ai-finder/', views.ai_finder_page, name='ai_finder_page'),
    path('api/ai-finder/', views.ai_finder_api, name='ai_finder_api'),
]