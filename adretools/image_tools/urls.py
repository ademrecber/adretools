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
    
    # English URLs (Primary)
    path('image-resize/', views.image_home, name='resize_image_en'),
    path('image-crop/', views.image_home, name='crop_image_en'),
    path('image-rotate/', views.image_home, name='rotate_image_en'),
    path('image-format-converter/', views.image_home, name='convert_image_en'),
    path('ico-creator/', views.image_home, name='create_ico_en'),
    path('image-compressor/', views.image_home, name='compress_image_en'),
    path('photo-resizer/', views.image_home, name='photo_resize_en'),
    path('reduce-image-size/', views.image_home, name='image_reduce_en'),
    path('jpg-to-png/', views.image_home, name='jpg_png_en'),
    path('free-image-editor/', views.image_home, name='free_image_editor_en'),
]