from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.contrib.sitemaps.views import sitemap
from core.sitemaps import StaticViewSitemap
from core.sitemaps import BlogPostSitemap

sitemaps = {
    'static': StaticViewSitemap,
}

if BlogPostSitemap:
    sitemaps['blog'] = BlogPostSitemap

urlpatterns = [
    # SEO
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    path('ads.txt', TemplateView.as_view(template_name='ads.txt', content_type='text/plain')),
]

urlpatterns += i18n_patterns(
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('pdf/', include('pdf_tools.urls')),
    path('image/', include('image_tools.urls')),
    path('qr/', include('qr_tools.urls')),
    path('svg/', include('svg_tools.urls')),
    path('text/', include('text_tools.urls')),
    path('color/', include('color_tools.urls')),
    path('url/', include('url_tools.urls')),
    path('password/', include('password_tools.urls')),
    path('converter/', include('converter_tools.urls')),
    path('horoscope/', include('horoscope_tools.urls')),
    path('network/', include('network_tools.urls')),
    path('dev/', include('dev_tools.urls')),
    path('calculator/', include('calculator_tools.urls')),
    path('random/', include('random_tools.urls')),
    path('blog/', include('blog.urls')),
    prefix_default_language=False,
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)