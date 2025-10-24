from django.http import HttpResponsePermanentRedirect
from django.conf import settings

class RedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # HTTP to HTTPS redirect
        if not request.is_secure() and not settings.DEBUG:
            return HttpResponsePermanentRedirect(
                'https://' + request.get_host() + request.get_full_path()
            )
        
        # www to non-www redirect
        host = request.get_host()
        if host.startswith('www.'):
            new_host = host[4:]  # Remove 'www.'
            protocol = 'https' if request.is_secure() else 'http'
            return HttpResponsePermanentRedirect(
                f'{protocol}://{new_host}{request.get_full_path()}'
            )
        
        response = self.get_response(request)
        return response