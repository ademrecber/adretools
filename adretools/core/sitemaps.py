from django.contrib.sitemaps import Sitemap
from django.urls import reverse

try:
    from blog.models import BlogPost
except ImportError:
    BlogPost = None

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
            
            # QR Tools SEO (doğru isimler)
            'qr_tools:qr_generator_tr', 'qr_tools:qr_generator_en',
            'qr_tools:barcode_generator_tr', 'qr_tools:barcode_generator_en',
            
            # Image Tools SEO
            'image_tools:resize_image_tr', 'image_tools:resize_image_en',
            'image_tools:crop_image_tr', 'image_tools:crop_image_en',
            'image_tools:compress_image_tr', 'image_tools:compress_image_en',
            
            # Password Tools SEO
            'password_tools:password_generator_tr', 'password_tools:password_generator_en',
            'password_tools:strong_password_tr', 'password_tools:strong_password_en',
            
            # Text Tools SEO
            'text_tools:word_counter_tr', 'text_tools:word_counter_en',
            'text_tools:text_analyzer_tr', 'text_tools:text_analyzer_en',
            
            # URL Tools SEO
            'url_tools:url_shortener_tr', 'url_tools:url_shortener_en',
            'url_tools:link_shortener_tr', 'url_tools:link_shortener_en',
            
            # Color Tools SEO
            'color_tools:color_picker_tr', 'color_tools:color_picker_en',
            'color_tools:hex_color_tr', 'color_tools:hex_color_en',
            
            # Calculator Tools SEO
            'calculator_tools:bmi_calculator', 'calculator_tools:bmi_calculator_tr',
            'calculator_tools:age_calculator', 'calculator_tools:age_calculator_tr',
            
            # Random Tools SEO
            'random_tools:random_number_seo', 'random_tools:random_number_tr',
            'random_tools:lucky_wheel_seo', 'random_tools:lucky_wheel_tr',
            
            # Converter Tools SEO
            'converter_tools:unit_converter_tr', 'converter_tools:unit_converter_en',
            'converter_tools:temperature_converter_tr', 'converter_tools:temperature_converter_en',
            
            # SVG Tools SEO
            'svg_tools:svg_editor_tr', 'svg_tools:svg_editor_en',
            'svg_tools:image_to_svg_tr', 'svg_tools:image_to_svg_en',
            
            # Horoscope Tools SEO
            'horoscope_tools:horoscope_calculator_tr', 'horoscope_tools:horoscope_calculator_en',
            
            # Blog SEO URLs
            'blog:blog_home', 'blog:blog_tr', 'blog:how_to_tr', 'blog:tool_guides_tr',
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

# BlogPostSitemap will be available when blog migrations are complete
if BlogPost is not None:
    class BlogPostSitemap(Sitemap):
        changefreq = 'weekly'
        priority = 0.9
        
        def items(self):
            try:
                return BlogPost.objects.filter(is_published=True)
            except:
                return []
        
        def lastmod(self, obj):
            return obj.updated_at
        
        def location(self, obj):
            return obj.get_absolute_url()
        
        def priority(self, obj):
            if hasattr(obj, 'is_featured') and obj.is_featured:
                return 1.0
            return 0.9