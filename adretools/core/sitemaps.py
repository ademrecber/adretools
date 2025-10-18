from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        # Sadece ana sayfalar (güvenli)
        return [
            'core:home',
            'qr_tools:home', 
            'image_tools:home', 
            'pdf_tools:home',
            'password_tools:home', 
            'calculator_tools:home', 
            'random_tools:home',
            'text_tools:home', 
            'url_tools:home', 
            'color_tools:home',
            'converter_tools:home', 
            'svg_tools:home', 
            'horoscope_tools:home',
            'network_tools:home', 
            'dev_tools:home',
        ]

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        # Popüler araçlara daha yüksek öncelik
        high_priority = [
            'qr_tools:qr_generator_tr', 'qr_tools:qr_generator_en',
            'image_tools:resize_image_tr', 'image_tools:resize_image_en', 
            'password_tools:password_generator_tr', 'password_tools:password_generator_en',
            'calculator_tools:bmi_calculator_tr', 'calculator_tools:bmi_calculator_seo',
            'random_tools:random_number_tr', 'random_tools:random_number_seo',
        ]
        
        if item in high_priority:
            return 1.0
        return 0.8