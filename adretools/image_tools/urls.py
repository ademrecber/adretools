from django.urls import path
from . import views

app_name = 'image_tools'

urlpatterns = [
    path('', views.image_home, name='home'),
    path('resize/', views.resize_image, name='resize'),
    path('crop/', views.crop_image, name='crop'),
    path('rotate/', views.rotate_image, name='rotate'),
    path('convert/', views.convert_format, name='convert'),
    path('ico/', views.create_ico, name='create_ico'),
    path('compress/', views.compress_image, name='compress'),
    
    # SEO optimized URLs
    path('resim-boyutlandir/', views.image_home, name='resize_image_tr'),
    path('image-resize/', views.image_home, name='resize_image_en'),
    path('resim-kirp/', views.image_home, name='crop_image_tr'),
    path('image-crop/', views.image_home, name='crop_image_en'),
    path('resim-dondur/', views.image_home, name='rotate_image_tr'),
    path('image-rotate/', views.image_home, name='rotate_image_en'),
    path('resim-format-donustur/', views.image_home, name='convert_image_tr'),
    path('image-format-converter/', views.image_home, name='convert_image_en'),
    path('ico-olustur/', views.image_home, name='create_ico_tr'),
    path('ico-creator/', views.image_home, name='create_ico_en'),
    path('resim-sikistir/', views.image_home, name='compress_image_tr'),
    path('image-compressor/', views.image_home, name='compress_image_en'),
    
    # Popüler arama terimleri
    path('foto-boyutlandir/', views.image_home, name='photo_resize_tr'),
    path('photo-resizer/', views.image_home, name='photo_resize_en'),
    path('resim-kucult/', views.image_home, name='image_reduce_tr'),
    path('reduce-image-size/', views.image_home, name='image_reduce_en'),
    path('jpg-png-donustur/', views.image_home, name='jpg_png_tr'),
    path('jpg-to-png/', views.image_home, name='jpg_png_en'),
    path('ucretsiz-resim-duzenle/', views.image_home, name='free_image_editor_tr'),
    path('free-image-editor/', views.image_home, name='free_image_editor_en'),
]