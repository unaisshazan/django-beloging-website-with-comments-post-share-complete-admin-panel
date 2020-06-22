# custom context processors
from django.conf import settings

def custom_context(request):
    """
    Custom items that are available to the templates
    """
    if settings.DEBUG and settings.DEBUG_IGNORE_DEMO_ACCOUNTS:
        demo = False
    else:
        demo = request.user.is_authenticated() and request.user.id in settings.DEMO_USERS
        
    return {
        'DJANGO_VER': 'django 1.8.7 LTS',
        'DEMO': demo
            }
