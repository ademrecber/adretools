from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from PIL import Image, ImageEnhance, ImageFilter
import io
import os

def image_home(request):
    tools = [
        {'name': 'Resize', 'id': 'resize', 'icon': 'fas fa-expand-arrows-alt', 'desc': 'Change image dimensions'},
        {'name': 'Crop', 'id': 'crop', 'icon': 'fas fa-crop', 'desc': 'Crop image from desired area'},
        {'name': 'Rotate', 'id': 'rotate', 'icon': 'fas fa-redo', 'desc': 'Rotate or flip image'},
        {'name': 'Format Convert', 'id': 'convert', 'icon': 'fas fa-exchange-alt', 'desc': 'Convert between JPG, PNG, WEBP'},
        {'name': 'Create ICO', 'id': 'ico', 'icon': 'fas fa-desktop', 'desc': 'JPG/PNG/SVG → ICO icon file'},
        {'name': 'Compress', 'id': 'compress', 'icon': 'fas fa-compress', 'desc': 'Reduce file size'},
    ]
    return render(request, 'image_tools/home.html', {'tools': tools})

@csrf_exempt
def resize_image(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    if 'image' not in request.FILES:
        return JsonResponse({'error': 'Image required'}, status=400)
    
    try:
        image_file = request.FILES['image']
        img = Image.open(image_file)
        
        # Boyut parametreleri
        width = request.POST.get('width')
        height = request.POST.get('height')
        percent = request.POST.get('percent')
        keep_ratio = request.POST.get('keep_ratio') == 'true'
        
        if percent:
            # Yüzde ile boyutlandır
            percent = float(percent) / 100
            new_width = int(img.width * percent)
            new_height = int(img.height * percent)
        elif width and height:
            new_width = int(width)
            new_height = int(height)
            
            if keep_ratio:
                # Oranı koruyarak boyutlandır
                img.thumbnail((new_width, new_height), Image.Resampling.LANCZOS)
                new_width, new_height = img.size
        else:
            return JsonResponse({'error': 'Size parameters required'}, status=400)
        
        # Boyutlandır
        if not (percent or keep_ratio):
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Kaydet
        output = io.BytesIO()
        format_type = 'PNG' if img.mode == 'RGBA' else 'JPEG'
        img.save(output, format=format_type, quality=95)
        output.seek(0)
        
        response = HttpResponse(output.getvalue(), content_type=f'image/{format_type.lower()}')
        response['Content-Disposition'] = f'attachment; filename="resized_{image_file.name}"'
        
        return response
        
    except Exception as e:
        return JsonResponse({'error': f'Resize error: {str(e)}'}, status=500)

@csrf_exempt
def crop_image(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    if 'image' not in request.FILES:
        return JsonResponse({'error': 'Image required'}, status=400)
    
    try:
        image_file = request.FILES['image']
        img = Image.open(image_file)
        
        # Kırpma parametreleri
        x = int(request.POST.get('x', 0))
        y = int(request.POST.get('y', 0))
        width = int(request.POST.get('width', img.width))
        height = int(request.POST.get('height', img.height))
        
        # Kırp
        cropped = img.crop((x, y, x + width, y + height))
        
        # Kaydet
        output = io.BytesIO()
        format_type = 'PNG' if cropped.mode == 'RGBA' else 'JPEG'
        cropped.save(output, format=format_type, quality=95)
        output.seek(0)
        
        response = HttpResponse(output.getvalue(), content_type=f'image/{format_type.lower()}')
        response['Content-Disposition'] = f'attachment; filename="cropped_{image_file.name}"'
        
        return response
        
    except Exception as e:
        return JsonResponse({'error': f'Crop error: {str(e)}'}, status=500)

@csrf_exempt
def rotate_image(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    if 'image' not in request.FILES:
        return JsonResponse({'error': 'Image required'}, status=400)
    
    try:
        image_file = request.FILES['image']
        img = Image.open(image_file)
        
        # Döndürme parametreleri
        angle = float(request.POST.get('angle', 0))
        flip_h = request.POST.get('flip_h') == 'true'
        flip_v = request.POST.get('flip_v') == 'true'
        
        # Döndür
        if angle != 0:
            img = img.rotate(-angle, expand=True, fillcolor='white')
        
        # Çevir
        if flip_h:
            img = img.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        if flip_v:
            img = img.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        
        # Kaydet
        output = io.BytesIO()
        format_type = 'PNG' if img.mode == 'RGBA' else 'JPEG'
        img.save(output, format=format_type, quality=95)
        output.seek(0)
        
        response = HttpResponse(output.getvalue(), content_type=f'image/{format_type.lower()}')
        response['Content-Disposition'] = f'attachment; filename="rotated_{image_file.name}"'
        
        return response
        
    except Exception as e:
        return JsonResponse({'error': f'Rotation error: {str(e)}'}, status=500)

@csrf_exempt
def convert_format(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    if 'image' not in request.FILES:
        return JsonResponse({'error': 'Image required'}, status=400)
    
    try:
        image_file = request.FILES['image']
        img = Image.open(image_file)
        
        # Format parametreleri
        target_format = request.POST.get('format', 'jpg').upper()
        quality = int(request.POST.get('quality', 85))
        keep_transparency = request.POST.get('transparency') == 'true'
        
        # Format dönüştürme
        if target_format == 'JPG':
            target_format = 'JPEG'
            if img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
        elif target_format == 'PNG' and not keep_transparency:
            img = img.convert('RGB')
        
        # Kaydet
        output = io.BytesIO()
        save_kwargs = {'format': target_format}
        
        if target_format in ['JPEG', 'WEBP']:
            save_kwargs['quality'] = quality
            save_kwargs['optimize'] = True
        
        img.save(output, **save_kwargs)
        output.seek(0)
        
        file_ext = target_format.lower().replace('jpeg', 'jpg')
        response = HttpResponse(output.getvalue(), content_type=f'image/{file_ext}')
        response['Content-Disposition'] = f'attachment; filename="converted.{file_ext}"'
        
        return response
        
    except Exception as e:
        return JsonResponse({'error': f'Conversion error: {str(e)}'}, status=500)

@csrf_exempt
def create_ico(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    if 'image' not in request.FILES:
        return JsonResponse({'error': 'File required'}, status=400)
    
    try:
        image_file = request.FILES['image']
        file_ext = image_file.name.lower().split('.')[-1]
        
        # Dosya türüne göre işle
        if file_ext == 'pdf':
            return JsonResponse({'error': 'PDF to ICO conversion is not supported'}, status=400)
        elif file_ext == 'svg':
            # SVG için cairosvg kullan
            from cairosvg import svg2png
            png_data = svg2png(bytestring=image_file.read())
            img = Image.open(io.BytesIO(png_data))
        else:
            # Normal resim dosyaları
            img = Image.open(image_file)
        
        # RGBA'ya çevir
        img = img.convert('RGBA')
        
        # ICO boyutları (16x16, 32x32, 48x48, 64x64, 128x128, 256x256)
        sizes = [(16,16), (32,32), (48,48), (64,64), (128,128), (256,256)]
        
        # Her boyut için resim oluştur
        ico_images = []
        for size in sizes:
            resized = img.resize(size, Image.Resampling.LANCZOS)
            ico_images.append(resized)
        
        # ICO dosyası oluştur
        output = io.BytesIO()
        ico_images[0].save(output, format='ICO', sizes=sizes, append_images=ico_images[1:])
        output.seek(0)
        
        response = HttpResponse(output.getvalue(), content_type='image/x-icon')
        response['Content-Disposition'] = f'attachment; filename="{image_file.name.rsplit(".", 1)[0]}.ico"'
        
        return response
        
    except Exception as e:
        return JsonResponse({'error': f'ICO creation error: {str(e)}'}, status=500)

@csrf_exempt
def compress_image(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    if 'image' not in request.FILES:
        return JsonResponse({'error': 'Image required'}, status=400)
    
    try:
        image_file = request.FILES['image']
        img = Image.open(image_file)
        
        # Sıkıştırma parametreleri
        quality = int(request.POST.get('quality', 70))
        target_size_mb = request.POST.get('target_size')
        
        # JPG'ye çevir (sıkıştırma için)
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
        
        # Hedef boyut varsa iteratif sıkıştır
        if target_size_mb:
            target_bytes = float(target_size_mb) * 1024 * 1024
            current_quality = quality
            
            while current_quality > 10:
                output = io.BytesIO()
                img.save(output, format='JPEG', quality=current_quality, optimize=True)
                
                if output.tell() <= target_bytes:
                    break
                    
                current_quality -= 5
                output.seek(0)
        else:
            output = io.BytesIO()
            img.save(output, format='JPEG', quality=quality, optimize=True)
        
        output.seek(0)
        
        response = HttpResponse(output.getvalue(), content_type='image/jpeg')
        response['Content-Disposition'] = f'attachment; filename="compressed_{image_file.name.rsplit(".", 1)[0]}.jpg"'
        
        return response
        
    except Exception as e:
        return JsonResponse({'error': f'Compression error: {str(e)}'}, status=500)