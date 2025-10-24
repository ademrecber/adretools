from django.urls import path
from . import views

app_name = 'svg_tools'

urlpatterns = [
    path('', views.svg_home, name='svg_home'),
    path('raster-to-svg/', views.raster_to_svg, name='raster_to_svg'),
    path('svg-to-raster/', views.svg_to_raster, name='svg_to_raster'),
    path('vector-trace/', views.vector_trace, name='vector_trace'),
    path('edit-svg/', views.edit_svg, name='edit_svg'),
    
    # English URLs (Primary)
    path('svg-editor/', views.svg_home, name='svg_editor_en'),
    path('image-to-svg/', views.svg_home, name='image_to_svg_en'),
    path('svg-to-png/', views.svg_home, name='svg_to_png_en'),
    path('vector-drawing/', views.svg_home, name='vector_drawing_en'),
]