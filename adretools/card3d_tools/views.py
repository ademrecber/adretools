from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.safestring import mark_safe
from PIL import Image
import io
import json
from .ai_depth import generate_depth_map, create_3d_layers
from .adre_generator import generate_adre_file

def card3d_home(request):
    return render(request, 'card3d_tools/home.html')

@csrf_exempt
def generate_3d_card(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    if 'image' not in request.FILES:
        return JsonResponse({'error': 'Image required'}, status=400)
    
    try:
        image_file = request.FILES['image']
        style = request.POST.get('style', 'modern')
        
        # Görsel işleme
        img = Image.open(image_file)
        
        # AI Depth Detection
        depth_map = generate_depth_map(img)
        
        # 3D Layers oluştur
        layers = create_3d_layers(img, depth_map)
        layers['has_back'] = False
        
        # ADRE formatında HTML dosyası oluştur
        adre_content = generate_adre_file(img, layers, style)
        
        # Binary olarak döndür
        response = HttpResponse(adre_content, content_type='application/octet-stream')
        response['Content-Disposition'] = 'attachment; filename="3d_card.html"'
        response['Content-Length'] = len(adre_content.encode('utf-8'))
        
        return response
        
    except Exception as e:
        return JsonResponse({'error': f'Generation error: {str(e)}'}, status=500)

