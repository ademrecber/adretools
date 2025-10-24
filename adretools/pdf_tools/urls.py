from django.urls import path
from django.views.generic import TemplateView
from django.http import HttpResponsePermanentRedirect
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
    
    # English URLs (Primary)
    path('merge-pdf/', views.pdf_home, name='merge_pdf_en'),
    path('split-pdf/', views.pdf_home, name='split_pdf_en'),
    path('encrypt-pdf/', views.pdf_home, name='encrypt_pdf_en'),
    path('watermark-pdf/', views.pdf_home, name='watermark_pdf_en'),
    path('compress-pdf/', views.pdf_home, name='compress_pdf_en'),
    path('pdf-to-word/', views.pdf_home, name='pdf_to_word_en'),
    path('pdf-to-excel/', views.pdf_home, name='pdf_to_excel_en'),
    
    # Turkish redirects to English
    path('pdf-birlestir/', lambda r: HttpResponsePermanentRedirect('/pdf/merge-pdf/'), name='merge_pdf_tr'),
    path('pdf-bol/', lambda r: HttpResponsePermanentRedirect('/pdf/split-pdf/'), name='split_pdf_tr'),
    path('pdf-sifrele/', lambda r: HttpResponsePermanentRedirect('/pdf/encrypt-pdf/'), name='encrypt_pdf_tr'),
    path('pdf-filigran/', lambda r: HttpResponsePermanentRedirect('/pdf/watermark-pdf/'), name='watermark_pdf_tr'),
    path('pdf-sikistir/', lambda r: HttpResponsePermanentRedirect('/pdf/compress-pdf/'), name='compress_pdf_tr'),
    path('pdf-word-donustur/', lambda r: HttpResponsePermanentRedirect('/pdf/pdf-to-word/'), name='pdf_to_word_tr'),
    path('pdf-excel-donustur/', lambda r: HttpResponsePermanentRedirect('/pdf/pdf-to-excel/'), name='pdf_to_excel_tr'),
    
    # Popüler arama terimleri
    path('ucretsiz-pdf-birlestir/', views.pdf_home, name='free_merge_pdf_tr'),
    path('free-pdf-merger/', views.pdf_home, name='free_merge_pdf_en'),
    path('online-pdf-duzenle/', views.pdf_home, name='online_pdf_editor_tr'),
    path('online-pdf-editor/', views.pdf_home, name='online_pdf_editor_en'),
]