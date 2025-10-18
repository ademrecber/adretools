from django.urls import path
from . import views

urlpatterns = [
    path('', views.text_home, name='text_home'),
    path('analyze/', views.analyze_text, name='analyze_text'),
    path('transform/', views.transform_text, name='transform_text'),
    path('encode/', views.encode_text, name='encode_text'),
    path('format/', views.format_text, name='format_text'),
    
    # SEO optimized URLs
    path('metin-analiz/', views.text_home, name='text_analyzer_tr'),
    path('text-analyzer/', views.text_home, name='text_analyzer_en'),
    path('kelime-sayaci/', views.text_home, name='word_counter_tr'),
    path('word-counter/', views.text_home, name='word_counter_en'),
    path('metin-donusturucu/', views.text_home, name='text_converter_tr'),
    path('text-converter/', views.text_home, name='text_converter_en'),
    path('base64-encode/', views.text_home, name='base64_encoder_en'),
    path('base64-kodlama/', views.text_home, name='base64_encoder_tr'),
]