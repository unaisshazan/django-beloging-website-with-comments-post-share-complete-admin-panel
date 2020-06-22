import calendar
import datetime

def last_day_of_prev_month(from_day):
    
    month = from_day.month
    if month == 1:
        prev_month = 12
        year = from_day.year - 1
    else:
        prev_month = month - 1
        year = from_day.year
        
    days_in_prev_month = calendar.monthrange(year,prev_month)[1]
    
    return datetime.datetime(year,prev_month,days_in_prev_month)

def last_day_of_month(year,month):
    
    days_in_month =  calendar.monthrange(year,month)[1]
    
    return datetime.datetime(year,month,days_in_month)
    