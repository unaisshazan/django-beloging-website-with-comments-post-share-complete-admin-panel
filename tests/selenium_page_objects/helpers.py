import datetime
import functools
from . import selenium_settings

def verify_browser(browser):
    
    for check_browser in selenium_settings.WEBDRIVERS.values():
        
        if isinstance(browser,check_browser):
            return True
        
    return False


def is_user_input_field(input_name):
    
    return not (len(input_name) < 1 or input_name in selenium_settings.EXCLUDE_FIELDS)
 
    

def full_url(url):
    
    protocol = 'https' if selenium_settings.USE_HTTPS else 'http'
    u = '{protocol}://{host}{url}'.format(protocol=protocol,host=selenium_settings.HOST,url=url)
    return u

def poll_dom(func,arg,timout):

    start = datetime.datetime.now()
    until = start + datetime.timedelta(0,timout) ## (days,seconds)
    crr = start

    while crr <= until:
        try:
            Lelements = func(arg)
            return Lelements
        except:
            pass

    return[]

def custom_test_sort(Ltests):
    """ with Ltests list of TestCase tests method ["test_foo","test_baz",...]
    call unittest.TestLoader.sortTestMethodsUsing = custom_test_sort(Ltests)
    to run tests by the Ltests order. In the example above, test_foo will run before test_baz
    TestCase tests not in list will be sorted as usual"""
    
    def sort_by_list_index(self,x,y):
        """ self when called by unittest TestLoader object"""
        if x in Ltests and y in Ltests:
            return cmp(Ltests.index(x),Ltests.index(y))
        else:
            return cmp(x,y)
        
    return sort_by_list_index

def element_exists(func):    
    @functools.wraps(func)
    def wrapper(*args,**kwargs):
        try:
            func(*args,**kwargs)
            return True
        except:
            return False
    return wrapper

        
        
        
        
