from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        # Ana sayfalar + çalışan SEO URL'leri
        return [
            # Ana sayfalar
            'core:home',
            'qr_tools:home', 'image_tools:home', 'pdf_tools:home',
            'password_tools:home', 'calculator_tools:home', 'random_tools:home',
            'text_tools:home', 'url_tools:home', 'color_tools:home',
            'converter_tools:home', 'svg_tools:home', 'horoscope_tools:home',
            'network_tools:home', 'dev_tools:home',
            'dev_tools:xml_formatter', 'dev_tools:invoice_viewer',
            
            # Global English URLs (Primary)
            'qr_tools:qr_generator_en', 'qr_tools:barcode_generator_en',
            'image_tools:resize_image_en', 'image_tools:crop_image_en', 'image_tools:compress_image_en',
            'password_tools:password_generator_en', 'password_tools:strong_password_en',
            'text_tools:word_counter_en', 'text_tools:text_analyzer_en',
            'url_tools:url_shortener_en', 'url_tools:link_shortener_en',
            'color_tools:color_picker_en', 'color_tools:hex_color_en',
            'calculator_tools:bmi_calculator', 'calculator_tools:age_calculator',
            'random_tools:random_number_seo', 'random_tools:lucky_wheel_seo',
            'converter_tools:unit_converter_en', 'converter_tools:temperature_converter_en',
            'svg_tools:svg_editor_en', 'svg_tools:image_to_svg_en',
            'horoscope_tools:horoscope_calculator_en',
            'pdf_tools:merge_pdf_en', 'pdf_tools:split_pdf_en',
            'pdf_tools:encrypt_pdf_en', 'pdf_tools:watermark_pdf_en',
            'pdf_tools:compress_pdf_en', 'pdf_tools:pdf_to_word_en',
            'pdf_tools:pdf_to_excel_en', 'pdf_tools:free_merge_pdf_en',
            'pdf_tools:online_pdf_editor_en',
        ]

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        # Popüler araçlara daha yüksek öncelik
        high_priority = [
            'qr_tools:qr_generator_en', 'qr_tools:barcode_generator_en',
            'image_tools:resize_image_en', 'image_tools:compress_image_en',
            'password_tools:password_generator_en',
            'calculator_tools:bmi_calculator', 'calculator_tools:age_calculator',
            'random_tools:random_number_seo',
            'pdf_tools:merge_pdf_en', 'pdf_tools:split_pdf_en',
            'text_tools:word_counter_en', 'converter_tools:unit_converter_en',
        ]
        
        if item in high_priority:
            return 1.0
        return 0.8