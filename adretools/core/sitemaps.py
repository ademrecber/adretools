from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        # Tüm SEO URL'leri
        return [
            # Ana sayfalar
            'core:home',
            
            # QR Tools
            'qr_tools:qr_generator_tr', 'qr_tools:qr_generator_en',
            'qr_tools:barcode_generator_tr', 'qr_tools:barcode_generator_en',
            
            # Image Tools  
            'image_tools:resize_image_tr', 'image_tools:resize_image_en',
            'image_tools:crop_image_tr', 'image_tools:crop_image_en',
            'image_tools:compress_image_tr', 'image_tools:compress_image_en',
            
            # PDF Tools
            'pdf_tools:split_pdf_seo',
            
            # Password Tools
            'password_tools:password_generator_tr', 'password_tools:password_generator_en',
            'password_tools:strong_password_tr', 'password_tools:strong_password_en',
            
            # Calculator Tools
            'calculator_tools:bmi_calculator_tr', 'calculator_tools:bmi_calculator_seo',
            'calculator_tools:age_calculator_tr', 'calculator_tools:age_calculator_seo',
            'calculator_tools:world_clock_tr', 'calculator_tools:world_clock_seo',
            
            # Random Tools
            'random_tools:random_number_tr', 'random_tools:random_number_seo',
            'random_tools:lucky_wheel_tr', 'random_tools:lucky_wheel_seo',
            'random_tools:name_picker_tr', 'random_tools:name_picker_seo',
            
            # Text Tools
            'text_tools:word_counter_tr', 'text_tools:word_counter_en',
            'text_tools:text_analyzer_tr', 'text_tools:text_analyzer_en',
            
            # URL Tools
            'url_tools:url_shortener_tr', 'url_tools:url_shortener_en',
            'url_tools:link_shortener_tr', 'url_tools:link_shortener_en',
            
            # Color Tools
            'color_tools:color_picker_tr', 'color_tools:color_picker_en',
            'color_tools:hex_color_tr', 'color_tools:hex_color_en',
            
            # Converter Tools
            'converter_tools:unit_converter_tr', 'converter_tools:unit_converter_en',
            'converter_tools:temperature_converter_tr', 'converter_tools:temperature_converter_en',
            
            # SVG Tools
            'svg_tools:svg_editor_tr', 'svg_tools:svg_editor_en',
            'svg_tools:image_to_svg_tr', 'svg_tools:image_to_svg_en',
            
            # Horoscope Tools
            'horoscope_tools:horoscope_calculator_tr', 'horoscope_tools:horoscope_calculator_en',
            'horoscope_tools:birth_date_horoscope_tr', 'horoscope_tools:birth_date_horoscope_en',
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