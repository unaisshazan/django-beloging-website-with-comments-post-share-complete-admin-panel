import datetime
from django.core.exceptions import ValidationError
from django.http import Http404

from ..utils.misc import last_day_of_month,last_day_of_prev_month

def verify_month_int(value):
    
    if value not in range(1,13):
        raise ValidationError(message='Please select a month')
    
def verify_month_is_before_this_month(year,month,raise_exception=True):
    
    t = datetime.datetime.today()
    if last_day_of_month(year,month) > last_day_of_prev_month(t):
        if raise_exception:
            raise ValidationError(message="The month is this month or after it")  
        else:
            return False
    else:
        return True
    
    
    
