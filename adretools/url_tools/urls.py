from django.urls import path
from . import views

app_name = 'url_tools'

urlpatterns = [
    path('', views.url_home, name='home'),
    path('shorten/', views.shorten_url, name='shorten_url'),
    path('stats/', views.get_stats, name='get_stats'),
    path('r/<str:short_code>/', views.redirect_url, name='redirect_url'),
    
    # English URLs (Primary)
    path('url-shortener/', views.url_home, name='url_shortener_en'),
    path('link-shortener/', views.url_home, name='link_shortener_en'),
    path('qr-code-link/', views.url_home, name='qr_link_en'),
]