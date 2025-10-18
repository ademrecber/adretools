from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import random
import string
import re

def password_home(request):
    return render(request, 'password_tools/home.html')

@csrf_exempt
def generate_password(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    try:
        length = int(request.POST.get('length', 12))
        include_uppercase = request.POST.get('uppercase') == 'true'
        include_lowercase = request.POST.get('lowercase') == 'true'
        include_numbers = request.POST.get('numbers') == 'true'
        include_symbols = request.POST.get('symbols') == 'true'
        exclude_similar = request.POST.get('exclude_similar') == 'true'
        
        if length < 4 or length > 128:
            return JsonResponse({'error': 'Password length must be between 4-128 characters'}, status=400)
        
        if not any([include_uppercase, include_lowercase, include_numbers, include_symbols]):
            return JsonResponse({'error': 'At least one character type must be selected'}, status=400)
        
        # Karakter setleri
        chars = ''
        if include_lowercase:
            chars += string.ascii_lowercase
        if include_uppercase:
            chars += string.ascii_uppercase
        if include_numbers:
            chars += string.digits
        if include_symbols:
            chars += '!@#$%^&*()_+-=[]{}|;:,.<>?'
        
        # Benzer karakterleri hariç tut
        if exclude_similar:
            similar_chars = 'il1Lo0O'
            chars = ''.join(c for c in chars if c not in similar_chars)
        
        # Şifre oluştur
        password = ''.join(random.choice(chars) for _ in range(length))
        
        # Güvenlik skoru hesapla
        score = calculate_password_strength(password)
        
        return JsonResponse({
            'password': password,
            'strength': score
        })
        
    except Exception as e:
        return JsonResponse({'error': f'Password generation error: {str(e)}'}, status=500)

@csrf_exempt
def check_password(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    password = request.POST.get('password', '')
    if not password:
        return JsonResponse({'error': 'Password required'}, status=400)
    
    try:
        strength = calculate_password_strength(password)
        return JsonResponse({'strength': strength})
    except Exception as e:
        return JsonResponse({'error': f'Password check error: {str(e)}'}, status=500)

def calculate_password_strength(password):
    score = 0
    feedback = []
    
    # Uzunluk kontrolü
    length = len(password)
    if length >= 8:
        score += 25
    elif length >= 6:
        score += 15
        feedback.append('Password should be at least 8 characters')
    else:
        score += 5
        feedback.append('Password is too short')
    
    # Karakter türü kontrolü
    has_lower = bool(re.search(r'[a-z]', password))
    has_upper = bool(re.search(r'[A-Z]', password))
    has_digit = bool(re.search(r'\d', password))
    has_symbol = bool(re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password))
    
    char_types = sum([has_lower, has_upper, has_digit, has_symbol])
    
    if char_types >= 4:
        score += 25
    elif char_types >= 3:
        score += 20
    elif char_types >= 2:
        score += 15
        feedback.append('Use more character types')
    else:
        score += 5
        feedback.append('Use uppercase, lowercase, numbers and symbols')
    
    # Tekrar eden karakter kontrolü
    unique_chars = len(set(password))
    if unique_chars / length > 0.7:
        score += 15
    elif unique_chars / length > 0.5:
        score += 10
    else:
        score += 5
        feedback.append('Too many repeating characters')
    
    # Yaygın kalıplar kontrolü
    common_patterns = ['123', 'abc', 'qwe', 'asd', 'password', 'admin']
    has_pattern = any(pattern in password.lower() for pattern in common_patterns)
    if not has_pattern:
        score += 15
    else:
        feedback.append('Avoid common patterns')
    
    # Ardışık karakter kontrolü
    sequential = 0
    for i in range(len(password) - 2):
        if ord(password[i+1]) == ord(password[i]) + 1 and ord(password[i+2]) == ord(password[i]) + 2:
            sequential += 1
    
    if sequential == 0:
        score += 20
    elif sequential <= 1:
        score += 10
        feedback.append('Reduce sequential characters')
    else:
        feedback.append('Too many sequential characters')
    
    # Skor sınırla
    score = min(100, max(0, score))
    
    # Güç seviyesi belirle
    if score >= 80:
        strength_level = 'Very Strong'
        color = 'success'
    elif score >= 60:
        strength_level = 'Strong'
        color = 'info'
    elif score >= 40:
        strength_level = 'Medium'
        color = 'warning'
    elif score >= 20:
        strength_level = 'Weak'
        color = 'danger'
    else:
        strength_level = 'Very Weak'
        color = 'danger'
    
    return {
        'score': score,
        'level': strength_level,
        'color': color,
        'feedback': feedback,
        'details': {
            'length': length,
            'has_lower': has_lower,
            'has_upper': has_upper,
            'has_digit': has_digit,
            'has_symbol': has_symbol,
            'unique_ratio': round(unique_chars / length * 100, 1)
        }
    }