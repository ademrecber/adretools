from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
import io
import base64
import xml.etree.ElementTree as ET

def svg_home(request):
    tools = [
        {'name': 'PNG/JPG to SVG', 'id': 'raster-to-svg', 'icon': 'fas fa-vector-square', 'desc': 'Convert raster image to SVG'},
        {'name': 'SVG to PNG/JPG', 'id': 'svg-to-raster', 'icon': 'fas fa-image', 'desc': 'Convert SVG to PNG/JPG'},
        {'name': 'SVG Edit', 'id': 'svg-edit', 'icon': 'fas fa-edit', 'desc': 'Edit SVG size and color'},
        {'name': 'Vector Trace', 'id': 'vector-trace', 'icon': 'fas fa-bezier-curve', 'desc': 'Convert image to vector SVG'},
    ]
    return render(request, 'svg_tools/home.html', {'tools': tools})

@csrf_exempt
def raster_to_svg(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    if 'image_file' not in request.FILES:
        return JsonResponse({'error': 'Image file required'}, status=400)
    
    try:
        image_file = request.FILES['image_file']
        mode = request.POST.get('mode', 'embed')
        
        img = Image.open(image_file)
        img = img.convert("RGBA")
        
        # Base64 embed modu - web uyumlu
        output = io.BytesIO()
        img.save(output, format='PNG')
        img_data = base64.b64encode(output.getvalue()).decode()
        
        svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="{img.width}" height="{img.height}" xmlns="http://www.w3.org/2000/svg">
    <image href="data:image/png;base64,{img_data}" width="{img.width}" height="{img.height}"/>
</svg>'''
        
        response = HttpResponse(svg_content, content_type='image/svg+xml')
        response['Content-Disposition'] = f'attachment; filename="{image_file.name.rsplit(".", 1)[0]}.svg"'
        return response

    except Exception as e:
        return JsonResponse({'error': f'Conversion error: {str(e)}'}, status=500)

@csrf_exempt
def svg_to_raster(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    if 'svg_file' not in request.FILES:
        return JsonResponse({'error': 'SVG file required'}, status=400)
    
    try:
        from cairosvg import svg2png, svg2jpeg
        
        svg_file = request.FILES['svg_file']
        output_format = request.POST.get('format', 'png')
        width = int(request.POST.get('width', 800))
        height = int(request.POST.get('height', 600))
        
        svg_content = svg_file.read()
        
        if output_format == 'png':
            output_data = svg2png(bytestring=svg_content, output_width=width, output_height=height)
            content_type = 'image/png'
            ext = 'png'
        else:
            output_data = svg2jpeg(bytestring=svg_content, output_width=width, output_height=height)
            content_type = 'image/jpeg'
            ext = 'jpg'
        
        response = HttpResponse(output_data, content_type=content_type)
        response['Content-Disposition'] = f'attachment; filename="{svg_file.name.rsplit(".", 1)[0]}.{ext}"'
        return response
        
    except Exception as e:
        return JsonResponse({'error': f'Conversion error: {str(e)}'}, status=500)

@csrf_exempt
def vector_trace(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    if 'image_file' not in request.FILES:
        return JsonResponse({'error': 'Image file required'}, status=400)
    
    try:
        image_file = request.FILES['image_file']
        detail_level = int(request.POST.get('detail_level', 5))
        
        img = Image.open(image_file)
        img = img.convert('RGBA')
        
        import numpy as np
        img_array = np.array(img)
        height, width = img_array.shape[:2]
        
        # Renk gruplarını tespit et
        unique_colors = {}
        for y in range(0, height, detail_level):
            for x in range(0, width, detail_level):
                r, g, b, a = img_array[y, x]
                if a > 128:  # Şeffaf olmayan pikseller
                    color_key = f'#{r:02x}{g:02x}{b:02x}'
                    if color_key not in unique_colors:
                        unique_colors[color_key] = []
                    unique_colors[color_key].append((x, y))
        
        # Her renk için path oluştur
        svg_paths = []
        for color, points in unique_colors.items():
            if len(points) > 0:
                # Noktalara göre rect'ler oluştur
                rects = []
                for x, y in points:
                    rects.append(f'M{x},{y} L{x+detail_level},{y} L{x+detail_level},{y+detail_level} L{x},{y+detail_level} Z')
                
                if rects:
                    path_data = ' '.join(rects)
                    svg_paths.append(f'<path d="{path_data}" fill="{color}"/>')
        
        svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
    {''.join(svg_paths)}
</svg>'''
        
        response = HttpResponse(svg_content, content_type='image/svg+xml')
        response['Content-Disposition'] = f'attachment; filename="traced_{image_file.name.rsplit(".", 1)[0]}.svg"'
        return response
        
    except Exception as e:
        return JsonResponse({'error': f'Vectorization error: {str(e)}'}, status=500)


@csrf_exempt
def edit_svg(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    if 'svg_file' not in request.FILES:
        return JsonResponse({'error': 'SVG file required'}, status=400)
    
    try:
        svg_file = request.FILES['svg_file']
        svg_content = svg_file.read().decode('utf-8')
        
        # Parametreler
        new_width = request.POST.get('new_width')
        new_height = request.POST.get('new_height')
        fill_color = request.POST.get('fill_color')
        stroke_color = request.POST.get('stroke_color')
        
        # SVG düzenle
        if new_width and new_height:
            import re
            svg_content = re.sub(r'width="[^"]*"', f'width="{new_width}"', svg_content)
            svg_content = re.sub(r'height="[^"]*"', f'height="{new_height}"', svg_content)
        
        if fill_color:
            svg_content = re.sub(r'fill="[^"]*"', f'fill="{fill_color}"', svg_content)
        
        if stroke_color:
            svg_content = re.sub(r'stroke="[^"]*"', f'stroke="{stroke_color}"', svg_content)
        
        response = HttpResponse(svg_content, content_type='image/svg+xml')
        response['Content-Disposition'] = f'attachment; filename="edited_{svg_file.name}"'
        
        return response
        
    except Exception as e:
        return JsonResponse({'error': f'Editing error: {str(e)}'}, status=500)