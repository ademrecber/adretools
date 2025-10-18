from django.shortcuts import render
from django.http import JsonResponse
from django.utils.translation import gettext as _
from datetime import datetime, date
import pytz

def calculator_home(request):
    tools = [
        {'name': _('BMI Calculator'), 'id': 'bmi', 'icon': 'fas fa-weight', 'desc': _('Calculate Body Mass Index')},
        {'name': _('Age Calculator'), 'id': 'age', 'icon': 'fas fa-birthday-cake', 'desc': _('Calculate age from birth date')},
        {'name': _('World Clock'), 'id': 'world-clock', 'icon': 'fas fa-globe', 'desc': _('World time zones')},
        {'name': _('Percentage Calculator'), 'id': 'percentage', 'icon': 'fas fa-percent', 'desc': _('Calculate percentages')},
        {'name': _('Date Calculator'), 'id': 'date', 'icon': 'fas fa-calendar', 'desc': _('Calculate days between dates')},
    ]
    return render(request, 'calculator_tools/home.html', {'tools': tools})

def bmi_calculator(request):
    return render(request, 'calculator_tools/bmi.html')

def age_calculator(request):
    return render(request, 'calculator_tools/age.html')

def world_clock(request):
    return render(request, 'calculator_tools/world_clock.html')