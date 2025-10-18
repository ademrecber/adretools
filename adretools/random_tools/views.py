from django.shortcuts import render
from django.utils.translation import gettext as _

def random_home(request):
    tools = [
        {'name': _('Random Number Generator'), 'id': 'random-number', 'icon': 'fas fa-hashtag', 'desc': _('Generate random numbers')},
        {'name': _('Lucky Wheel'), 'id': 'lucky-wheel', 'icon': 'fas fa-dharmachakra', 'desc': _('Spin the wheel of fortune')},
        {'name': _('Dice Roller'), 'id': 'dice', 'icon': 'fas fa-dice', 'desc': _('Roll virtual dice')},
        {'name': _('Name Picker'), 'id': 'name-picker', 'icon': 'fas fa-users', 'desc': _('Professional lottery system')},
    ]
    return render(request, 'random_tools/home.html', {'tools': tools})