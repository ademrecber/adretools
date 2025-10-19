from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.blog_home, name='blog_home'),
    path('<slug:slug>/', views.blog_post, name='blog_post'),
    
    # SEO URLs
    path('blog/', views.blog_home, name='blog_tr'),
    path('nasil-kullanilir/', views.blog_home, name='how_to_tr'),
    path('arac-rehberleri/', views.blog_home, name='tool_guides_tr'),
]