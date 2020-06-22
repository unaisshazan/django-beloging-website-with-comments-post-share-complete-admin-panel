import django
import datetime
from django.conf import settings
def set_env():
    """ load django, and set site specific environment"""
    django.setup()
    
    
def format_today_full(text):
    
    t = datetime.date.today().strftime(settings.DATE_FULL_STRFTIME)
    return text.format(today=t)

def format_today(text):
    
    return text.format(today=str(datetime.date.today()))
    