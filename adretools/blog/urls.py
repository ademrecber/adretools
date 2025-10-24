from django.urls import path
from django.http import HttpResponsePermanentRedirect
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.blog_home, name='blog_home'),
    path('<slug:slug>/', views.blog_post, name='blog_post'),
    
    # Redirects to main blog
    path('rehberler/', lambda r: HttpResponsePermanentRedirect('/blog/')),
    path('nasil-kullanilir/', lambda r: HttpResponsePermanentRedirect('/blog/')),
    path('arac-rehberleri/', lambda r: HttpResponsePermanentRedirect('/blog/')),
]