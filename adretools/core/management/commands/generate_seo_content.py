from django.core.management.base import BaseCommand
from blog.models import BlogPost

class Command(BaseCommand):
    help = 'Generate SEO-optimized blog content'

    def handle(self, *args, **options):
        posts = [
            {
                'title': 'PDF Birleştirme Nasıl Yapılır? Ücretsiz Online Araç',
                'slug': 'pdf-birlestirme-nasil-yapilir',
                'content': 'PDF dosyalarını birleştirmek için AdreTools kullanın. Ücretsiz, hızlı ve güvenli.',
                'excerpt': 'PDF dosyalarını ücretsiz birleştirme rehberi',
                'meta_description': 'PDF birleştirme nasıl yapılır? Ücretsiz online araç ile PDF dosyalarını birleştirin.',
                'meta_keywords': 'pdf birleştir, pdf merge, ücretsiz pdf araçları',
                'category': 'tutorials'
            },
            {
                'title': 'QR Kod Nasıl Oluşturulur? Ücretsiz QR Kod Üretici',
                'slug': 'qr-kod-nasil-olusturulur',
                'content': 'QR kod oluşturmak için AdreTools QR kod üreticisini kullanın.',
                'excerpt': 'QR kod oluşturma rehberi ve ipuçları',
                'meta_description': 'QR kod oluşturma rehberi. URL, WiFi, vCard QR kodları ücretsiz oluşturun.',
                'meta_keywords': 'qr kod oluştur, qr kod üretici, ücretsiz qr kod',
                'category': 'guides'
            }
        ]

        for post_data in posts:
            post, created = BlogPost.objects.get_or_create(
                slug=post_data['slug'],
                defaults=post_data
            )
            if created:
                self.stdout.write(f'Created: {post.title}')

        self.stdout.write(self.style.SUCCESS('SEO content generated!'))