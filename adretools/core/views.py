from django.shortcuts import render
from django.utils.translation import gettext as _

def home(request):
    tools = [
        {'name': _('PDF Tools'), 'url': '/pdf/', 'icon': 'fas fa-file-pdf', 'desc': _('Split, merge, convert PDF files')},
        {'name': _('Image Tools'), 'url': '/image/', 'icon': 'fas fa-image', 'desc': _('Resize images, change formats')},
        {'name': _('QR & Barcode'), 'url': '/qr/', 'icon': 'fas fa-qrcode', 'desc': _('Generate QR codes, read barcodes')},
        {'name': _('SVG Tools'), 'url': '/svg/', 'icon': 'fas fa-vector-square', 'desc': _('Edit SVG files')},
        {'name': _('Text Tools'), 'url': '/text/', 'icon': 'fas fa-font', 'desc': _('Analyze and convert text')},
        {'name': _('Color Picker'), 'url': '/color/', 'icon': 'fas fa-palette', 'desc': _('Pick colors from images and analyze')},
        {'name': _('URL Shortener'), 'url': '/url/', 'icon': 'fas fa-link', 'desc': _('Shorten long links and generate QR')},
        {'name': _('Password Generator'), 'url': '/password/', 'icon': 'fas fa-key', 'desc': _('Generate strong passwords and security check')},
        {'name': _('Unit Converter'), 'url': '/converter/', 'icon': 'fas fa-exchange-alt', 'desc': _('Convert length, weight, temperature')},
        {'name': _('Horoscope Calculator'), 'url': '/horoscope/', 'icon': 'fas fa-star', 'desc': _('Calculate zodiac sign and traits by birth date')},
        {'name': _('Network Tools'), 'url': '/network/', 'icon': 'fas fa-network-wired', 'desc': _('IP lookup, domain check, port scan')},
        {'name': _('Developer Tools'), 'url': '/dev/', 'icon': 'fas fa-code', 'desc': _('JSON, Hash, Regex, SQL tools')},
        {'name': _('Calculator Tools'), 'url': '/calculator/', 'icon': 'fas fa-calculator', 'desc': _('BMI, Age, World Clock calculators')},
        {'name': _('Random Tools'), 'url': '/random/', 'icon': 'fas fa-dice', 'desc': _('Random number, lucky wheel, lottery system')},
    ]
    return render(request, 'core/home.html', {'tools': tools})

def terms_of_service(request):
    return render(request, 'terms-of-service.html')

def cookie_policy(request):
    return render(request, 'cookie-policy.html')