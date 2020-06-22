import re
from django import template
from django.conf import settings

register = template.Library()
regex_page = re.compile("page=[0-9]+")

@register.filter
def intmonth(value):
    
    try:
        return ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"][int(value)-1]
    except:
        return value
    
@register.filter
def currencyformat(value):
    try:
        float(value)
    except:
        value = 0
    return '{:0,}'.format(int(round(value)))


@register.filter
def abs_value(value):
    try:
        float(value)
    except:
        value = 0
  
    return abs(value)


@register.filter
def date_format(value):
    return value.strftime(settings.DATE_FULL_STRFTIME)

@register.filter
def striftrue(value,arg):
    """ only for strict boolean, will not convert a True/False typecast"""
    return arg if  value is True else ""

@register.filter
def add_page_arg(url,page_index):
    
    if regex_page.search(url) != None:
        return regex_page.sub("page=%s"%page_index,url)
    else:
        url_base = "%s&&page=%s" if "?" in url else "%s?page=%s"
        return url_base%(url,page_index,)
    
from django.contrib.messages import constants
Dmessage = {constants.DEBUG:"bg-info",
            constants.INFO:"bg-primary",
            constants.SUCCESS:"bg-success",
            constants.WARNING:"bg-warning",
            constants.ERROR:"bg-danger"}
@register.filter
def django_to_bootstrap_message_class(value):
    
    return Dmessage.get(value,"")
    
    

   
    
    


