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
        
        # Try Gemini API first
        if GEMINI_AVAILABLE and settings.GEMINI_API_KEY:
            try:
                genai.configure(api_key=settings.GEMINI_API_KEY)
                model = genai.GenerativeModel('gemini-pro')
                
                prompt = f"""
User needs: "{query}"

Provide 5 specific AI tools for this exact need. For each tool, provide:
1. Name
2. What it does (specific to the user's need)
3. How to use it (step-by-step)
4. Pricing
5. Website URL

Format as JSON:
[
  {{
    "name": "Tool Name",
    "description": "Specific description for user's need",
    "how_to_use": "Step 1: ... Step 2: ... Step 3: ...",
    "pricing": "Free/Paid/Freemium with details",
    "url": "https://example.com"
  }}
]

Only return valid JSON array.
"""
                
                response = model.generate_content(prompt)
                ai_tools = json.loads(response.text)
                
                return JsonResponse({
                    'query': query,
                    'tools': ai_tools,
                    'count': len(ai_tools)
                })
                
            except Exception as gemini_error:
                # Fall back to manual recommendations
                pass
        
        # Fallback: Manual recommendations based on query
        query_lower = query.lower()
        
        if 'video' in query_lower:
            tools = [
                {
                    "name": "Runway ML",
                    "description": "AI video generation and editing platform",
                    "how_to_use": "1. Sign up at runway.ml 2. Choose 'Gen-2' for text-to-video 3. Enter your prompt 4. Wait 1-2 minutes for generation 5. Download your video",
                    "pricing": "Free: 125 credits/month, Paid: $12-35/month",
                    "url": "https://runway.ml"
                },
                {
                    "name": "Pika Labs",
                    "description": "Text-to-video AI generator",
                    "how_to_use": "1. Join Discord server 2. Use /create command 3. Type your video description 4. Wait for generation 5. Download result",
                    "pricing": "Free with Discord, Paid plans available",
                    "url": "https://pika.art"
                },
                {
                    "name": "Synthesia",
                    "description": "AI avatar video creation",
                    "how_to_use": "1. Choose avatar 2. Write script 3. Select voice 4. Generate video 5. Download or share",
                    "pricing": "Paid: $22-67/month",
                    "url": "https://synthesia.io"
                }
            ]
        elif 'image' in query_lower or 'photo' in query_lower:
            tools = [
                {
                    "name": "Midjourney",
                    "description": "High-quality AI image generation",
                    "how_to_use": "1. Join Discord 2. Use /imagine command 3. Type detailed prompt 4. Choose variation 5. Upscale image",
                    "pricing": "Paid: $10-60/month",
                    "url": "https://midjourney.com"
                },
                {
                    "name": "DALL-E 3",
                    "description": "OpenAI's image generator",
                    "how_to_use": "1. Go to ChatGPT Plus 2. Ask to create image 3. Describe what you want 4. Get 4 variations 5. Download",
                    "pricing": "ChatGPT Plus: $20/month",
                    "url": "https://chat.openai.com"
                }
            ]
        else:
            tools = [
                {
                    "name": "ChatGPT",
                    "description": "AI assistant for your specific need",
                    "how_to_use": "1. Go to chat.openai.com 2. Create account 3. Type your request clearly 4. Ask follow-up questions 5. Copy results",
                    "pricing": "Free version available, Plus: $20/month",
                    "url": "https://chat.openai.com"
                }
            ]
        
        return JsonResponse({
            'query': query,
            'tools': tools,
            'count': len(tools)
        })
            
    except Exception as e:
        return JsonResponse({'error': f'AI Finder error: {str(e)}'}, status=500)