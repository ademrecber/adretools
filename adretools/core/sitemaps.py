from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        # Tüm ana sayfalar ve SEO URL'leri
        urls = [
            # Ana sayfalar
            'core:home',
            'qr_tools:home', 'image_tools:home', 'pdf_tools:home',
            'password_tools:home', 'calculator_tools:home', 'random_tools:home',
            'text_tools:home', 'url_tools:home', 'color_tools:home',
            'converter_tools:home', 'svg_tools:home', 'horoscope_tools:home',
            'network_tools:home', 'dev_tools:home',
        ]
        
        # SEO URL'leri ekle (sadece çalışanlar)
        seo_urls = [
            # QR Tools SEO
            'qr_tools:qr_kod_olustur', 'qr_tools:qr_code_generator',
            'qr_tools:barkod_olustur', 'qr_tools:barcode_generator',
            
            # Image Tools SEO
            'image_tools:resim_boyutlandir', 'image_tools:image_resize',
            'image_tools:resim_kirp', 'image_tools:image_crop',
            'image_tools:resim_sikistir', 'image_tools:image_compressor',
            'image_tools:ico_olustur', 'image_tools:ico_creator',
            
            # Password Tools SEO
            'password_tools:sifre_olustur', 'password_tools:password_generator',
            'password_tools:guclu_sifre', 'password_tools:strong_password',
            
            # Text Tools SEO
            'text_tools:kelime_sayici', 'text_tools:word_counter',
            'text_tools:metin_analiz', 'text_tools:text_analyzer',
            
            # URL Tools SEO
            'url_tools:url_kisalt', 'url_tools:url_shortener',
            'url_tools:link_kisalt', 'url_tools:link_shortener',
            
            # Color Tools SEO
            'color_tools:renk_secici', 'color_tools:color_picker',
            'color_tools:hex_renk', 'color_tools:hex_color',
            
            # Calculator Tools SEO
            'calculator_tools:bmi_hesapla', 'calculator_tools:bmi_calculator',
            'calculator_tools:yas_hesapla', 'calculator_tools:age_calculator',
            
            # Random Tools SEO
            'random_tools:rastgele_sayi', 'random_tools:random_number',
            'random_tools:sans_carkı', 'random_tools:lucky_wheel',
            'random_tools:isim_secici', 'random_tools:name_picker',
            
            # Converter Tools SEO
            'converter_tools:unit_converter_tr', 'converter_tools:unit_converter_en',
            'converter_tools:temperature_converter_tr', 'converter_tools:temperature_converter_en',
            
            # SVG Tools SEO
            'svg_tools:svg_editor_tr', 'svg_tools:svg_editor_en',
            'svg_tools:image_to_svg_tr', 'svg_tools:image_to_svg_en',
        ]
        
        # Sadece çalışan URL'leri ekle
        for url in seo_urls:
            try:
                from django.urls import reverse
                reverse(url)
                urls.append(url)
            except:
                pass  # URL çalışmıyorsa atla
                
        return urls

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