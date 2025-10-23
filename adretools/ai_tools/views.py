from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

def ai_home(request):
    tools = [
        {'name': 'AI Finder', 'id': 'ai-finder', 'icon': 'fas fa-search', 'desc': 'Find the best AI tools for your needs'},
    ]
    return render(request, 'ai_tools/home.html', {'tools': tools})

def ai_finder_page(request):
    return render(request, 'ai_tools/ai_finder.html', {
        'title': 'AI Finder - Find Best AI Tools for Your Needs',
        'description': 'Discover the perfect AI tools and applications for your specific requirements. Get personalized recommendations.',
        'keywords': 'ai finder, ai tools, artificial intelligence, ai recommendations'
    })

@csrf_exempt
def ai_finder_api(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    try:
        data = json.loads(request.body)
        query = data.get('query', '').strip()
        
        if not query:
            return JsonResponse({'error': 'Query required'}, status=400)
        
        # Check if Gemini is available
        if not GEMINI_AVAILABLE:
            return JsonResponse({'error': 'AI service not available - missing library'}, status=503)
        
        if not settings.GEMINI_API_KEY:
            return JsonResponse({'error': 'AI service not configured'}, status=503)
        
        # Use Gemini API
        genai.configure(api_key=settings.GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-pro')
        
        prompt = f"""
User query: "{query}"

Find 8-10 best AI tools/websites for this specific need. Include both popular and newer tools. For each tool provide:

1. Name (exact tool name)
2. Description (what it does for this specific need)
3. How to use (detailed step-by-step instructions)
4. Pricing (specific prices, free tiers, etc.)
5. Website URL (real working URL)

Include tools like Sora, Veo, Luma Dream Machine, Kling AI for video needs.
Include latest and most relevant tools available in 2024.

Return ONLY valid JSON array:
[
  {{
    "name": "Tool Name",
    "description": "What it does for user's specific need",
    "how_to_use": "Step 1: ... Step 2: ... Step 3: ...",
    "pricing": "Detailed pricing info",
    "url": "https://real-website.com"
  }}
]
"""
        
        response = model.generate_content(prompt)
        
        # Clean and parse response
        response_text = response.text.strip()
        if response_text.startswith('```json'):
            response_text = response_text[7:-3]
        elif response_text.startswith('```'):
            response_text = response_text[3:-3]
        
        ai_tools = json.loads(response_text)
        
        return JsonResponse({
            'query': query,
            'tools': ai_tools,
            'count': len(ai_tools)
        })
            
    except Exception as e:
        return JsonResponse({'error': f'AI Finder error: {str(e)}'}, status=500)