from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def converter_home(request):
    return render(request, 'converter_tools/home.html')

@csrf_exempt
def convert_unit(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    try:
        category = request.POST.get('category')
        from_unit = request.POST.get('from_unit')
        to_unit = request.POST.get('to_unit')
        value = float(request.POST.get('value', 0))
        
        if not all([category, from_unit, to_unit]):
            return JsonResponse({'error': 'All fields are required'}, status=400)
        
        # Dönüştürme işlemi
        result = perform_conversion(category, from_unit, to_unit, value)
        
        return JsonResponse({
            'result': result,
            'formatted': format_result(result)
        })
        
    except ValueError:
        return JsonResponse({'error': 'Invalid number format'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'Conversion error: {str(e)}'}, status=500)

def perform_conversion(category, from_unit, to_unit, value):
    # Dönüştürme tabloları (metre cinsinden)
    conversions = {
        'length': {
            'mm': 0.001,
            'cm': 0.01,
            'm': 1,
            'km': 1000,
            'inch': 0.0254,
            'ft': 0.3048,
            'yard': 0.9144,
            'mile': 1609.34
        },
        'weight': {
            'mg': 0.000001,
            'g': 0.001,
            'kg': 1,
            'ton': 1000,
            'oz': 0.0283495,
            'lb': 0.453592,
            'stone': 6.35029
        },
        'temperature': {
            'celsius': lambda c: c,
            'fahrenheit': lambda f: (f - 32) * 5/9,
            'kelvin': lambda k: k - 273.15
        },
        'area': {
            'mm2': 0.000001,
            'cm2': 0.0001,
            'm2': 1,
            'km2': 1000000,
            'inch2': 0.00064516,
            'ft2': 0.092903,
            'acre': 4046.86,
            'hectare': 10000
        },
        'volume': {
            'ml': 0.001,
            'l': 1,
            'm3': 1000,
            'gallon_us': 3.78541,
            'gallon_uk': 4.54609,
            'pint': 0.473176,
            'quart': 0.946353,
            'cup': 0.236588
        },
        'speed': {
            'mps': 1,
            'kmh': 0.277778,
            'mph': 0.44704,
            'knot': 0.514444,
            'fps': 0.3048
        }
    }
    
    if category == 'temperature':
        # Sıcaklık özel işlem gerektirir
        return convert_temperature(from_unit, to_unit, value)
    
    if category not in conversions:
        raise ValueError(f'Unsupported category: {category}')
    
    units = conversions[category]
    
    if from_unit not in units or to_unit not in units:
        raise ValueError('Unsupported unit')
    
    # Temel birime çevir, sonra hedef birime çevir
    base_value = value * units[from_unit]
    result = base_value / units[to_unit]
    
    return result

def convert_temperature(from_unit, to_unit, value):
    # Önce Celsius'a çevir
    if from_unit == 'celsius':
        celsius = value
    elif from_unit == 'fahrenheit':
        celsius = (value - 32) * 5/9
    elif from_unit == 'kelvin':
        celsius = value - 273.15
    else:
        raise ValueError('Unsupported temperature unit')
    
    # Celsius'tan hedef birime çevir
    if to_unit == 'celsius':
        return celsius
    elif to_unit == 'fahrenheit':
        return celsius * 9/5 + 32
    elif to_unit == 'kelvin':
        return celsius + 273.15
    else:
        raise ValueError('Unsupported temperature unit')

def format_result(result):
    # Sonucu uygun formatta göster
    if abs(result) >= 1000000:
        return f"{result:.2e}"
    elif abs(result) >= 1000:
        return f"{result:,.2f}"
    elif abs(result) >= 1:
        return f"{result:.4f}".rstrip('0').rstrip('.')
    elif abs(result) >= 0.0001:
        return f"{result:.6f}".rstrip('0').rstrip('.')
    else:
        return f"{result:.2e}"