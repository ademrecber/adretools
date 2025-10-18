from django.urls import path
from . import views

urlpatterns = [
    path('', views.svg_home, name='svg_home'),
    path('raster-to-svg/', views.raster_to_svg, name='raster_to_svg'),
    path('svg-to-raster/', views.svg_to_raster, name='svg_to_raster'),
    path('vector-trace/', views.vector_trace, name='vector_trace'),
    path('edit-svg/', views.edit_svg, name='edit_svg'),
    
    # SEO optimized URLs
    path('svg-duzenleyici/', views.svg_home, name='svg_editor_tr'),
    path('svg-editor/', views.svg_home, name='svg_editor_en'),
    path('resim-svg-donustur/', views.svg_home, name='image_to_svg_tr'),
    path('image-to-svg/', views.svg_home, name='image_to_svg_en'),
    path('svg-png-donustur/', views.svg_home, name='svg_to_png_tr'),
    path('svg-to-png/', views.svg_home, name='svg_to_png_en'),
    path('vektor-cizim/', views.svg_home, name='vector_drawing_tr'),
    path('vector-drawing/', views.svg_home, name='vector_drawing_en'),
]