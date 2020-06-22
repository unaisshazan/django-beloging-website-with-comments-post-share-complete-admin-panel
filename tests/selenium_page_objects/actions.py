import re
from .exceptions import NoActionMethod
class SeleniumWebActionBase(object):
    
    def __init__(self,browser):
        self.browser = browser
    
    def run(self,*args,**kwargs):
        
        if kwargs.has_key("browser"):
            self.browser = kwargs['browser']
            kwargs.pop('browser')
        
        action_method =  getattr(self,self._first_action())
        self.browser = action_method(*args,**kwargs)
        
        return self.browser
    
    def _first_action(self): 
        
        r = re.compile("^action")
        try:
            return [x for x in dir(self) if r.match(x)][0]
        except:
            raise NoActionMethod(["No method starts with 'action'"])
        
        