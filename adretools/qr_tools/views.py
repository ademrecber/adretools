from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer, CircleModuleDrawer, SquareModuleDrawer
from PIL import Image, ImageDraw
import io
import tempfile
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import barcode
from barcode.writer import ImageWriter

def qr_home(request):
    tools = [
        {'name': 'Generate QR', 'id': 'generate', 'icon': 'fas fa-qrcode', 'desc': 'Create QR code from text/URL'},
        {'name': 'Read QR', 'id': 'read', 'icon': 'fas fa-camera', 'desc': 'Read and decode QR code'},
        {'name': 'Generate Barcode', 'id': 'barcode', 'icon': 'fas fa-barcode', 'desc': 'Create barcode'},
    ]
    return render(request, 'qr_tools/home.html', {'tools': tools})

@csrf_exempt
def generate_qr(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    content = request.POST.get('content', '')
    if not content:
        return JsonResponse({'error': 'Content required'}, status=400)
    
    try:
        # QR ayarları
        size = int(request.POST.get('size', 400))
        error_correction_map = {
            'L': qrcode.constants.ERROR_CORRECT_L,
            'M': qrcode.constants.ERROR_CORRECT_M,
            'Q': qrcode.constants.ERROR_CORRECT_Q,
            'H': qrcode.constants.ERROR_CORRECT_H
        }
        error_correction = error_correction_map.get(request.POST.get('error_correction', 'M'))
        
        # Hex renkleri RGB'ye çevir
        def hex_to_rgb(hex_color):
            hex_color = hex_color.lstrip('#')
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        foreground = hex_to_rgb(request.POST.get('foreground', '#000000'))
        background = hex_to_rgb(request.POST.get('background', '#ffffff'))
        style = request.POST.get('style', 'square')
        
        # QR kod oluştur
        qr = qrcode.QRCode(
            version=1,
            error_correction=error_correction,
            box_size=size//25,
            border=4,
        )
        qr.add_data(content)
        qr.make(fit=True)
        
        # Stil seçimi
        module_drawer = SquareModuleDrawer()
        
        if style == 'round':
            module_drawer = RoundedModuleDrawer()
        elif style == 'dot':
            module_drawer = CircleModuleDrawer()
        
        # QR görsel oluştur
        img = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=module_drawer,
            fill_color=foreground,
            back_color=background
        )
        
        # Logo ekle
        if 'logo' in request.FILES:
            logo = Image.open(request.FILES['logo'])
            
            # Logo boyutunu QR boyutuna ve stiline göre ayarla
            if style == 'round' or style == 'dot':
                logo_size = min(img.size[0], img.size[1]) // 8  # Yuvarlak için daha küçük
            else:
                logo_size = min(img.size[0], img.size[1]) // 6  # Kare için normal
            
            # Logo'yu yeniden boyutlandır
            logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
            
            # QR stiline göre logo şekli
            if style == 'round' or style == 'dot':
                # Yuvarlak maske oluştur (daha küçük)
                mask_size = int(logo_size * 0.8)  # %80 boyut
                mask = Image.new('L', (logo_size, logo_size), 0)
                draw = ImageDraw.Draw(mask)
                margin = (logo_size - mask_size) // 2
                draw.ellipse((margin, margin, logo_size - margin, logo_size - margin), fill=255)
                
                # Logo'yu yuvarlak yap
                logo_round = Image.new('RGBA', (logo_size, logo_size), (0, 0, 0, 0))
                logo_round.paste(logo, (0, 0))
                logo_round.putalpha(mask)
                logo = logo_round
            
            # Beyaz arka plan ekle (QR okuma için)
            bg_img = Image.new('RGBA', (logo_size + 8, logo_size + 8), background)
            if style == 'round' or style == 'dot':
                # Yuvarlak beyaz arka plan
                draw = ImageDraw.Draw(bg_img)
                draw.ellipse((0, 0, logo_size + 8, logo_size + 8), fill=background)
            
            # Logo pozisyonu (merkez)
            bg_pos = ((img.size[0] - (logo_size + 8)) // 2, (img.size[1] - (logo_size + 8)) // 2)
            logo_pos = ((img.size[0] - logo_size) // 2, (img.size[1] - logo_size) // 2)
            
            # Önce arka planı yapıştır
            img.paste(bg_img, bg_pos)
            # Sonra logo'yu yapıştır
            if logo.mode == 'RGBA':
                img.paste(logo, logo_pos, logo)
            else:
                img.paste(logo, logo_pos)
        
        # PNG olarak kaydet
        output = io.BytesIO()
        img.save(output, format='PNG')
        output.seek(0)
        
        return HttpResponse(output.getvalue(), content_type='image/png')
        
    except Exception as e:
        return JsonResponse({'error': f'QR generation error: {str(e)}'}, status=500)

@csrf_exempt
def download_qr(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    content = request.POST.get('content', '')
    format_type = request.POST.get('format', 'png')
    
    if not content:
        return JsonResponse({'error': 'Content required'}, status=400)
    
    try:
        # QR ayarları
        size = int(request.POST.get('size', 400))
        error_correction_map = {
            'L': qrcode.constants.ERROR_CORRECT_L,
            'M': qrcode.constants.ERROR_CORRECT_M,
            'Q': qrcode.constants.ERROR_CORRECT_Q,
            'H': qrcode.constants.ERROR_CORRECT_H
        }
        error_correction = error_correction_map.get(request.POST.get('error_correction', 'M'))
        
        # Hex renkleri RGB'ye çevir
        def hex_to_rgb(hex_color):
            hex_color = hex_color.lstrip('#')
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        foreground = hex_to_rgb(request.POST.get('foreground', '#000000'))
        background = hex_to_rgb(request.POST.get('background', '#ffffff'))
        style = request.POST.get('style', 'square')
        
        # QR kod oluştur
        qr = qrcode.QRCode(
            version=1,
            error_correction=error_correction,
            box_size=size//25,
            border=4,
        )
        qr.add_data(content)
        qr.make(fit=True)
        
        # Stil seçimi
        module_drawer = SquareModuleDrawer()
        
        if style == 'round':
            module_drawer = RoundedModuleDrawer()
        elif style == 'dot':
            module_drawer = CircleModuleDrawer()
        
        # QR görsel oluştur
        img = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=module_drawer,
            fill_color=foreground,
            back_color=background
        )
        
        # Logo ekle
        if 'logo' in request.FILES:
            logo = Image.open(request.FILES['logo'])
            
            # Logo boyutunu QR boyutuna ve stiline göre ayarla
            if style == 'round' or style == 'dot':
                logo_size = min(img.size[0], img.size[1]) // 8  # Yuvarlak için daha küçük
            else:
                logo_size = min(img.size[0], img.size[1]) // 6  # Kare için normal
            
            # Logo'yu yeniden boyutlandır
            logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
            
            # QR stiline göre logo şekli
            if style == 'round' or style == 'dot':
                # Yuvarlak maske oluştur (daha küçük)
                mask_size = int(logo_size * 0.8)  # %80 boyut
                mask = Image.new('L', (logo_size, logo_size), 0)
                draw = ImageDraw.Draw(mask)
                margin = (logo_size - mask_size) // 2
                draw.ellipse((margin, margin, logo_size - margin, logo_size - margin), fill=255)
                
                # Logo'yu yuvarlak yap
                logo_round = Image.new('RGBA', (logo_size, logo_size), (0, 0, 0, 0))
                logo_round.paste(logo, (0, 0))
                logo_round.putalpha(mask)
                logo = logo_round
            
            # Beyaz arka plan ekle (QR okuma için)
            bg_img = Image.new('RGBA', (logo_size + 8, logo_size + 8), background)
            if style == 'round' or style == 'dot':
                # Yuvarlak beyaz arka plan
                draw = ImageDraw.Draw(bg_img)
                draw.ellipse((0, 0, logo_size + 8, logo_size + 8), fill=background)
            
            # Logo pozisyonu (merkez)
            bg_pos = ((img.size[0] - (logo_size + 8)) // 2, (img.size[1] - (logo_size + 8)) // 2)
            logo_pos = ((img.size[0] - logo_size) // 2, (img.size[1] - logo_size) // 2)
            
            # Önce arka planı yapıştır
            img.paste(bg_img, bg_pos)
            # Sonra logo'yu yapıştır
            if logo.mode == 'RGBA':
                img.paste(logo, logo_pos, logo)
            else:
                img.paste(logo, logo_pos)
        
        output = io.BytesIO()
        
        if format_type == 'png':
            img.save(output, format='PNG')
            content_type = 'image/png'
        elif format_type == 'jpg':
            # JPG için beyaz arka plan
            if img.mode in ('RGBA', 'LA', 'P'):
                background_img = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background_img.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background_img
            img.save(output, format='JPEG', quality=95)
            content_type = 'image/jpeg'
        elif format_type == 'svg':
            # SVG için basit çözüm
            qr_simple = qrcode.QRCode(version=1, box_size=10, border=4)
            qr_simple.add_data(content)
            qr_simple.make(fit=True)
            
            svg_img = qr_simple.make_image(image_factory=qrcode.image.svg.SvgPathImage)
            output.write(svg_img.to_string().encode('utf-8'))
            content_type = 'image/svg+xml'
        elif format_type == 'pdf':
            # PDF oluştur
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_img:
                img.save(temp_img.name, format='PNG')
                temp_img_path = temp_img.name
            
            pdf_canvas = canvas.Canvas(output, pagesize=letter)
            pdf_canvas.drawImage(temp_img_path, 100, 400, width=size, height=size)
            pdf_canvas.save()
            
            os.unlink(temp_img_path)
            content_type = 'application/pdf'
        
        output.seek(0)
        
        response = HttpResponse(output.getvalue(), content_type=content_type)
        response['Content-Disposition'] = f'attachment; filename="qr_code.{format_type}"'
        
        return response
        
    except Exception as e:
        return JsonResponse({'error': f'Download error: {str(e)}'}, status=500)

@csrf_exempt
def read_qr(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    if 'image' not in request.FILES:
        return JsonResponse({'error': 'Image required'}, status=400)
    
    try:
        # OpenCV ile QR okuma
        import cv2
        import numpy as np
        from PIL import Image
        
        # Resmi oku
        image_file = request.FILES['image']
        image = Image.open(image_file)
        
        # OpenCV formatına çevir
        opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        # QR kod dedektörü oluştur
        qr_detector = cv2.QRCodeDetector()
        
        # QR kodu oku
        data, vertices_array, binary_qrcode = qr_detector.detectAndDecode(opencv_image)
        
        if data:
            return JsonResponse({'content': data})
        else:
            return JsonResponse({'error': 'QR code not found or could not be read'}, status=400)
            
    except ImportError:
        return JsonResponse({'error': 'OpenCV package not found. Install with pip install opencv-python.'}, status=500)
    except Exception as e:
        return JsonResponse({'error': f'QR reading error: {str(e)}'}, status=500)

@csrf_exempt
def generate_barcode(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    barcode_type = request.POST.get('type', 'code128')
    data = request.POST.get('data', '')
    
    if not data:
        return JsonResponse({'error': 'Barcode data required'}, status=400)
    
    try:
        # Barkod türü seçimi
        barcode_class = None
        if barcode_type == 'code128':
            barcode_class = barcode.Code128
        elif barcode_type == 'ean13':
            barcode_class = barcode.EAN13
        elif barcode_type == 'upc':
            barcode_class = barcode.UPCA
        elif barcode_type == 'code39':
            barcode_class = barcode.Code39
        
        if not barcode_class:
            return JsonResponse({'error': 'Invalid barcode type'}, status=400)
        
        # Barkod oluştur
        barcode_instance = barcode_class(data, writer=ImageWriter())
        
        # Resim olarak kaydet
        output = io.BytesIO()
        barcode_instance.write(output)
        output.seek(0)
        
        return HttpResponse(output.getvalue(), content_type='image/png')
        
    except Exception as e:
        return JsonResponse({'error': f'Barcode generation error: {str(e)}'}, status=500)

@csrf_exempt
def download_barcode(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    barcode_type = request.POST.get('type', 'code128')
    data = request.POST.get('data', '')
    format_type = request.POST.get('format', 'png')
    
    if not data:
        return JsonResponse({'error': 'Barcode data required'}, status=400)
    
    try:
        # Barkod türü seçimi
        barcode_class = None
        if barcode_type == 'code128':
            barcode_class = barcode.Code128
        elif barcode_type == 'ean13':
            barcode_class = barcode.EAN13
        elif barcode_type == 'upc':
            barcode_class = barcode.UPCA
        elif barcode_type == 'code39':
            barcode_class = barcode.Code39
        
        if not barcode_class:
            return JsonResponse({'error': 'Invalid barcode type'}, status=400)
        
        # Barkod oluştur
        barcode_instance = barcode_class(data, writer=ImageWriter())
        
        output = io.BytesIO()
        
        if format_type == 'png':
            barcode_instance.write(output)
            content_type = 'image/png'
        elif format_type == 'jpg':
            # PNG oluştur sonra JPG'ye çevir
            temp_output = io.BytesIO()
            barcode_instance.write(temp_output)
            temp_output.seek(0)
            
            img = Image.open(temp_output)
            if img.mode in ('RGBA', 'LA', 'P'):
                background_img = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background_img.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background_img
            img.save(output, format='JPEG', quality=95)
            content_type = 'image/jpeg'
        elif format_type == 'pdf':
            # PNG oluştur sonra PDF'e ekle
            temp_output = io.BytesIO()
            barcode_instance.write(temp_output)
            temp_output.seek(0)
            
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_img:
                temp_img.write(temp_output.getvalue())
                temp_img_path = temp_img.name
            
            pdf_canvas = canvas.Canvas(output, pagesize=letter)
            pdf_canvas.drawImage(temp_img_path, 100, 400, width=400, height=100)
            pdf_canvas.save()
            
            os.unlink(temp_img_path)
            content_type = 'application/pdf'
        
        output.seek(0)
        
        response = HttpResponse(output.getvalue(), content_type=content_type)
        response['Content-Disposition'] = f'attachment; filename="barcode.{format_type}"'
        
        return response
        
    except Exception as e:
        return JsonResponse({'error': f'Barcode download error: {str(e)}'}, status=500)