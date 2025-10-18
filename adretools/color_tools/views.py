from django.shortcuts import render

def color_home(request):
    return render(request, 'color_tools/home.html')