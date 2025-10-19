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
    
    # SEO optimized URLs
    path('pdf-birlestir/', views.pdf_home, name='merge_pdf_tr'),
    path('merge-pdf/', views.pdf_home, name='merge_pdf_en'),
    path('pdf-bol/', views.pdf_home, name='split_pdf_tr'),
    path('split-pdf/', views.pdf_home, name='split_pdf_en'),
    path('pdf-sifrele/', views.pdf_home, name='encrypt_pdf_tr'),
    path('encrypt-pdf/', views.pdf_home, name='encrypt_pdf_en'),
    path('pdf-filigran/', views.pdf_home, name='watermark_pdf_tr'),
    path('watermark-pdf/', views.pdf_home, name='watermark_pdf_en'),
    path('pdf-sikistir/', views.pdf_home, name='compress_pdf_tr'),
    path('compress-pdf/', views.pdf_home, name='compress_pdf_en'),
    path('pdf-word-donustur/', views.pdf_home, name='pdf_to_word_tr'),
    path('pdf-to-word/', views.pdf_home, name='pdf_to_word_en'),
    path('pdf-excel-donustur/', views.pdf_home, name='pdf_to_excel_tr'),
    path('pdf-to-excel/', views.pdf_home, name='pdf_to_excel_en'),
    
    # Popüler arama terimleri
    path('ucretsiz-pdf-birlestir/', views.pdf_home, name='free_merge_pdf_tr'),
    path('free-pdf-merger/', views.pdf_home, name='free_merge_pdf_en'),
    path('online-pdf-duzenle/', views.pdf_home, name='online_pdf_editor_tr'),
    path('online-pdf-editor/', views.pdf_home, name='online_pdf_editor_en'),
]