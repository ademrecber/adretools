from django.utils import translation
from django.conf import settings

class AutoLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Kullanıcının dil tercihi session'da varsa onu kullan
        if 'django_language' in request.session:
            language = request.session['django_language']
            translation.activate(language)
            request.LANGUAGE_CODE = language
        else:
            # Accept-Language header'ından dil algıla
            accept_language = request.META.get('HTTP_ACCEPT_LANGUAGE', '')
            
            # Desteklenen diller
            supported_languages = dict(settings.LANGUAGES)
            
            # En uygun dili bul
            best_language = 'en'  # varsayılan
            
            if accept_language:
                # Accept-Language: tr-TR,tr;q=0.9,en;q=0.8,en-US;q=0.7
                languages = accept_language.split(',')
                for lang in languages:
                    lang_code = lang.split(';')[0].strip().split('-')[0].lower()
                    if lang_code in supported_languages:
                        best_language = lang_code
                        break
            
            # Dili aktif et
            translation.activate(best_language)
            request.LANGUAGE_CODE = best_language
            request.session['django_language'] = best_language

        response = self.get_response(request)
        translation.deactivate()
        return response