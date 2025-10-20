from django.urls import path
from . import views

app_name = 'dev_tools'

urlpatterns = [
    path('', views.dev_home, name='home'),
    
    # SEO optimized pages
    path('json-formatter/', views.json_formatter_page, name='json_formatter_page'),
    path('hash-generator/', views.hash_generator_page, name='hash_generator_page'),
    path('regex-tester/', views.regex_tester_page, name='regex_tester_page'),
    path('base64-encoder/', views.base64_encoder_page, name='base64_encoder_page'),
    path('url-encoder/', views.url_encoder_page, name='url_encoder_page'),
    path('html-encoder/', views.html_encoder_page, name='html_encoder_page'),
    path('sql-formatter/', views.sql_formatter_page, name='sql_formatter_page'),
    path('timestamp-converter/', views.timestamp_converter_page, name='timestamp_converter_page'),
    path('xml-formatter/', views.xml_formatter_page, name='xml_formatter_page'),
    path('invoice-viewer/', views.invoice_viewer_page, name='invoice_viewer_page'),
    
    # API endpoints
    path('api/json-formatter/', views.json_formatter_api, name='json_formatter_api'),
    path('api/hash-generator/', views.hash_generator_api, name='hash_generator_api'),
    path('api/regex-tester/', views.regex_tester_api, name='regex_tester_api'),
    path('api/base64-encoder/', views.base64_encoder_api, name='base64_encoder_api'),
    path('api/url-encoder/', views.url_encoder_api, name='url_encoder_api'),
    path('api/html-encoder/', views.html_encoder_api, name='html_encoder_api'),
    path('api/sql-formatter/', views.sql_formatter_api, name='sql_formatter_api'),
    path('api/timestamp-converter/', views.timestamp_converter_api, name='timestamp_converter_api'),
]