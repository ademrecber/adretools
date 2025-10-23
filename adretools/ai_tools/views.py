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
        
        # Always return fallback results for now
        fallback_tools = [
            {
                "name": "ChatGPT",
                "description": "Advanced AI chatbot for conversations and text generation",
                "use_cases": "Writing, coding, analysis, Q&A",
                "pricing": "Freemium",
                "url": "https://chat.openai.com"
            },
            {
                "name": "Claude",
                "description": "AI assistant for analysis, writing, and coding",
                "use_cases": "Research, writing, programming help",
                "pricing": "Freemium",
                "url": "https://claude.ai"
            },
            {
                "name": "Midjourney",
                "description": "AI image generation from text prompts",
                "use_cases": "Art creation, design, illustrations",
                "pricing": "Paid",
                "url": "https://midjourney.com"
            },
            {
                "name": "Canva AI",
                "description": "AI-powered design and content creation",
                "use_cases": "Graphic design, presentations, social media",
                "pricing": "Freemium",
                "url": "https://canva.com"
            },
            {
                "name": "Grammarly",
                "description": "AI writing assistant for grammar and style",
                "use_cases": "Writing improvement, proofreading",
                "pricing": "Freemium",
                "url": "https://grammarly.com"
            }
        ]
        
        return JsonResponse({
            'query': query,
            'tools': fallback_tools,
            'count': len(fallback_tools),
            'note': 'Popular AI tools for your needs'
        })
            
    except Exception as e:
        return JsonResponse({'error': f'AI Finder error: {str(e)}'}, status=500)