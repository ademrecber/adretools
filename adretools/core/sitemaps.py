from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        # Sadece çalışan URL'ler
        return [
            # Ana sayfalar
            'core:home',
            
            # QR Tools
            'qr_tools:home',
            
            # Image Tools  
            'image_tools:home',
            
            # PDF Tools
            'pdf_tools:home',
            
            # Password Tools
            'password_tools:home',
            
            # Calculator Tools
            'calculator_tools:home',
            
            # Random Tools
            'random_tools:home',
            
            # Text Tools
            'text_tools:home',
            
            # URL Tools
            'url_tools:home',
            
            # Color Tools
            'color_tools:home',
            
            # Converter Tools
            'converter_tools:home',
            
            # SVG Tools
            'svg_tools:home',
            
            # Horoscope Tools
            'horoscope_tools:home',
            
            # Network Tools
            'network_tools:home',
            
            # Dev Tools
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