from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json
import google.generativeai as genai

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
        
        # Configure Gemini
        genai.configure(api_key=settings.GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-pro')
        
        # AI Finder prompt
        prompt = f"""
        User is looking for AI tools for: "{query}"
        
        Please provide 5 best AI tools/websites for this need. For each tool, provide:
        1. Name
        2. Brief description (what it does)
        3. Best use cases
        4. Pricing (Free/Paid/Freemium)
        5. Website URL (if known, otherwise use placeholder)
        
        Format as JSON array:
        [
            {{
                "name": "Tool Name",
                "description": "What this AI tool does",
                "use_cases": "Best for...",
                "pricing": "Free/Paid/Freemium",
                "url": "https://example.com"
            }}
        ]
        
        Only return the JSON array, no other text.
        """
        
        response = model.generate_content(prompt)
        
        # Parse AI response
        try:
            ai_tools = json.loads(response.text)
            return JsonResponse({
                'query': query,
                'tools': ai_tools,
                'count': len(ai_tools)
            })
        except json.JSONDecodeError:
            # Fallback if JSON parsing fails
            return JsonResponse({
                'query': query,
                'tools': [
                    {
                        "name": "ChatGPT",
                        "description": "Advanced AI chatbot for conversations and text generation",
                        "use_cases": "Writing, coding, analysis, Q&A",
                        "pricing": "Freemium",
                        "url": "https://chat.openai.com"
                    },
                    {
                        "name": "Midjourney",
                        "description": "AI image generation from text prompts",
                        "use_cases": "Art creation, design, illustrations",
                        "pricing": "Paid",
                        "url": "https://midjourney.com"
                    }
                ],
                'count': 2,
                'note': 'Fallback results - AI response parsing failed'
            })
            
    except Exception as e:
        return JsonResponse({'error': f'AI Finder error: {str(e)}'}, status=500)