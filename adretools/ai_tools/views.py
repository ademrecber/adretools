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
        
        # Use Gemini API with rate limiting
        genai.configure(api_key=settings.GEMINI_API_KEY)
        
        # Use gemini-pro (stable free model)
        model = genai.GenerativeModel('gemini-pro')
        
        # Add generation config for better rate limiting
        generation_config = {
            'temperature': 0.7,
            'top_p': 0.8,
            'top_k': 40,
            'max_output_tokens': 2048,
        }
        
        prompt = f"""
User needs: "{query}"

Find the best current AI tools for this specific need. Include both popular and newest available tools. For each tool provide:

1. Name
2. Description (specific to user's need)
3. How to use (step-by-step)
4. Pricing
5. Website URL

Return ONLY valid JSON array:
[
  {{
    "name": "Tool Name",
    "description": "What it does for user's need",
    "how_to_use": "Step 1: ... Step 2: ... Step 3: ...",
    "pricing": "Pricing details",
    "url": "https://website.com"
  }}
]
"""
        
        response = model.generate_content(
            prompt,
            generation_config=generation_config
        )
        
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
        error_msg = str(e).lower()
        
        # Handle different types of API errors
        if '429' in error_msg or 'quota' in error_msg or 'rate limit' in error_msg:
            return JsonResponse({
                'error': 'API rate limit exceeded. Please wait a moment and try again.',
                'retry_after': 60,
                'type': 'rate_limit'
            }, status=429)
        elif 'api key' in error_msg or 'authentication' in error_msg:
            return JsonResponse({
                'error': 'API authentication failed. Please contact support.',
                'type': 'auth_error'
            }, status=401)
        elif 'blocked' in error_msg or 'safety' in error_msg:
            return JsonResponse({
                'error': 'Request blocked by safety filters. Please rephrase your query.',
                'type': 'safety_error'
            }, status=400)
        else:
            return JsonResponse({
                'error': f'AI service error: {str(e)}',
                'type': 'general_error'
            }, status=500)