from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from .models import ShortenedURL
import qrcode
import io
import base64
from urllib.parse import urlparse

def url_home(request):
    return render(request, 'url_tools/home.html')

@csrf_exempt
def shorten_url(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    original_url = request.POST.get('url', '').strip()
    if not original_url:
        return JsonResponse({'error': 'URL required'}, status=400)
    
    # URL doğrulama
    if not original_url.startswith(('http://', 'https://')):
        original_url = 'https://' + original_url
    
    try:
        parsed = urlparse(original_url)
        if not parsed.netloc:
            return JsonResponse({'error': 'Invalid URL format'}, status=400)
    except:
        return JsonResponse({'error': 'Invalid URL'}, status=400)
    
    # Mevcut URL kontrolü
    existing = ShortenedURL.objects.filter(original_url=original_url).first()
    if existing:
        shortened_url = existing
    else:
        shortened_url = ShortenedURL.objects.create(original_url=original_url)
    
    # Kısa URL oluştur
    short_url = request.build_absolute_uri(reverse('redirect_url', args=[shortened_url.short_code]))
    
    # QR kod oluştur
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(short_url)
    qr.make(fit=True)
    
    qr_img = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    qr_img.save(buffer, format='PNG')
    qr_data = base64.b64encode(buffer.getvalue()).decode()
    
    return JsonResponse({
        'short_url': short_url,
        'short_code': shortened_url.short_code,
        'original_url': original_url,
        'qr_code': f'data:image/png;base64,{qr_data}',
        'click_count': shortened_url.click_count
    })

def redirect_url(request, short_code):
    url_obj = get_object_or_404(ShortenedURL, short_code=short_code)
    url_obj.click_count += 1
    url_obj.save()
    return redirect(url_obj.original_url)

@csrf_exempt
def get_stats(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    short_code = request.POST.get('code', '').strip()
    if not short_code:
        return JsonResponse({'error': 'Short code required'}, status=400)
    
    try:
        url_obj = ShortenedURL.objects.get(short_code=short_code)
        return JsonResponse({
            'short_code': url_obj.short_code,
            'original_url': url_obj.original_url,
            'click_count': url_obj.click_count,
            'created_at': url_obj.created_at.strftime('%d.%m.%Y %H:%M')
        })
    except ShortenedURL.DoesNotExist:
        return JsonResponse({'error': 'Short code not found'}, status=404)