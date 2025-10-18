from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import re
import json
import hashlib
import base64
from urllib.parse import quote, unquote
import html

def text_home(request):
    return render(request, 'text_tools/home.html')

@csrf_exempt
def analyze_text(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    text = request.POST.get('text', '')
    if not text:
        return JsonResponse({'error': 'Text required'}, status=400)
    
    # Temel sayımlar
    char_count = len(text)
    char_no_spaces = len(text.replace(' ', ''))
    word_count = len(text.split())
    line_count = len(text.splitlines())
    paragraph_count = len([p for p in text.split('\n\n') if p.strip()])
    
    # Rakam ve harf sayısı
    digit_count = sum(c.isdigit() for c in text)
    letter_count = sum(c.isalpha() for c in text)
    
    # En uzun kelime
    words = text.split()
    longest_word = max(words, key=len) if words else ''
    
    # Ortalama kelime uzunluğu
    avg_word_length = sum(len(word) for word in words) / len(words) if words else 0
    
    return JsonResponse({
        'char_count': char_count,
        'char_no_spaces': char_no_spaces,
        'word_count': word_count,
        'line_count': line_count,
        'paragraph_count': paragraph_count,
        'digit_count': digit_count,
        'letter_count': letter_count,
        'longest_word': longest_word,
        'avg_word_length': round(avg_word_length, 2)
    })

@csrf_exempt
def transform_text(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    text = request.POST.get('text', '')
    transform_type = request.POST.get('type', '')
    
    if not text:
        return JsonResponse({'error': 'Text required'}, status=400)
    
    try:
        if transform_type == 'uppercase':
            result = text.upper()
        elif transform_type == 'lowercase':
            result = text.lower()
        elif transform_type == 'title':
            result = text.title()
        elif transform_type == 'reverse':
            result = text[::-1]
        elif transform_type == 'slug':
            result = re.sub(r'[^\w\s-]', '', text.lower())
            result = re.sub(r'[-\s]+', '-', result).strip('-')
        elif transform_type == 'clean_spaces':
            result = re.sub(r'\s+', ' ', text).strip()
        elif transform_type == 'clean_special':
            result = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        elif transform_type == 'clean_html':
            result = html.unescape(re.sub(r'<[^>]+>', '', text))
        else:
            return JsonResponse({'error': 'Invalid transformation type'}, status=400)
        
        return JsonResponse({'result': result})
        
    except Exception as e:
        return JsonResponse({'error': f'Transformation error: {str(e)}'}, status=500)

@csrf_exempt
def encode_text(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    text = request.POST.get('text', '')
    encode_type = request.POST.get('type', '')
    
    if not text:
        return JsonResponse({'error': 'Text required'}, status=400)
    
    try:
        if encode_type == 'base64_encode':
            result = base64.b64encode(text.encode()).decode()
        elif encode_type == 'base64_decode':
            result = base64.b64decode(text.encode()).decode()
        elif encode_type == 'url_encode':
            result = quote(text)
        elif encode_type == 'url_decode':
            result = unquote(text)
        elif encode_type == 'md5':
            result = hashlib.md5(text.encode()).hexdigest()
        elif encode_type == 'sha256':
            result = hashlib.sha256(text.encode()).hexdigest()
        else:
            return JsonResponse({'error': 'Invalid encoding type'}, status=400)
        
        return JsonResponse({'result': result})
        
    except Exception as e:
        return JsonResponse({'error': f'Encoding error: {str(e)}'}, status=500)

@csrf_exempt
def format_text(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    text = request.POST.get('text', '')
    format_type = request.POST.get('type', '')
    
    if not text:
        return JsonResponse({'error': 'Text required'}, status=400)
    
    try:
        if format_type == 'json_format':
            parsed = json.loads(text)
            result = json.dumps(parsed, indent=2, ensure_ascii=False)
        elif format_type == 'json_minify':
            parsed = json.loads(text)
            result = json.dumps(parsed, separators=(',', ':'), ensure_ascii=False)
        else:
            return JsonResponse({'error': 'Invalid format type'}, status=400)
        
        return JsonResponse({'result': result})
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'Format error: {str(e)}'}, status=500)