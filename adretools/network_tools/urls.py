from django.urls import path
from . import views

app_name = 'network_tools'

urlpatterns = [
    path('', views.network_home, name='home'),
    
    # SEO optimized pages
    path('ip-lookup/', views.ip_lookup_page, name='ip_lookup_page'),
    path('domain-checker/', views.domain_checker_page, name='domain_checker_page'),
    path('port-scanner/', views.port_scanner_page, name='port_scanner_page'),
    path('ping-test/', views.ping_test_page, name='ping_test_page'),
    path('speed-test/', views.speed_test_page, name='speed_test_page'),
    
    # API endpoints
    path('api/ip-lookup/', views.ip_lookup_api, name='ip_lookup_api'),
    path('api/domain-checker/', views.domain_checker_api, name='domain_checker_api'),
    path('api/port-scanner/', views.port_scanner_api, name='port_scanner_api'),
    path('api/ping-test/', views.ping_test_api, name='ping_test_api'),
    path('api/speed-test/', views.speed_test_api, name='speed_test_api'),
]