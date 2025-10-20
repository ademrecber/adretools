from django.conf import settings

def seo_context(request):
    """Global SEO context for all templates"""
    return {
        'site_name': 'AdreTools',
        'site_url': 'https://adretools.com',
        'default_image': 'https://adretools.com/static/images/og-image.png',
        'twitter_handle': '@adretools',
        'fb_app_id': '',  # Facebook App ID if available
    }