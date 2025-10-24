from django.urls import path
from . import views

app_name = 'qr_tools'

urlpatterns = [
    path('', views.qr_home, name='home'),
    path('generate/', views.generate_qr, name='generate_qr'),
    path('download/', views.download_qr, name='download_qr'),
    path('read/', views.read_qr, name='read_qr'),
    path('barcode/', views.generate_barcode, name='generate_barcode'),
    path('barcode-download/', views.download_barcode, name='download_barcode'),
    
    # English URLs (Primary)
    path('qr-code-generator/', views.qr_home, name='qr_generator_en'),
    path('barcode-generator/', views.qr_home, name='barcode_generator_en'),
    path('qr-code-reader/', views.qr_home, name='qr_reader_en'),
    path('free-qr-code/', views.qr_home, name='free_qr_en'),
    path('online-qr-generator/', views.qr_home, name='online_qr_en'),
    path('wifi-qr-code/', views.qr_home, name='wifi_qr_en'),
]