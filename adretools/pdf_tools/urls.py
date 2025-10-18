from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'pdf_tools'

urlpatterns = [
    path('', views.pdf_home, name='home'),
    path('convert-to-word/', views.convert_pdf_to_word, name='convert_to_word'),
    path('convert-to-excel/', views.convert_pdf_to_excel, name='convert_to_excel'),
    path('convert-to-pdf/', views.convert_word_to_pdf, name='convert_to_pdf'),
    path('encrypt/', views.encrypt_pdf, name='encrypt_pdf'),
    path('add-watermark/', views.add_watermark, name='add_watermark'),
    path('split/', views.split_pdf, name='split_pdf'),
    path('merge/', views.merge_pdf, name='merge_pdf'),
    path('compress/', views.compress_pdf, name='compress_pdf'),
    
    # SEO optimized English pages
    path('split-pdf-online/', TemplateView.as_view(template_name='pdf_tools/split.html'), name='split_pdf_seo'),
]