from .wrapper import SeleniumWrapper
from .forms_html import is_user_input_field
from .helpers import verify_browser
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import InvalidElementStateException
from .exceptions import BrowserError
from .selenium_settings import WEBDRIVERS


class WebElementBase(object):
    '''application element which may not correspond to an HTML tags'''
    
    def __init__(self,*args,**kwargs):
        
        try:
            browser = kwargs['browser']
            assert verify_browser(browser)
            self.browser = browser
            self.wrapper = SeleniumWrapper(browser)
            
        except:
            raise BrowserError,(['No Browser'])

class WebElementHtmlBase(WebElementBase):
    
    _elemnt_type = None
    element = None
    
    def __init__(self,*args,**kwargs):
        super(WebElementHtmlBase,self).__init__(*args,**kwargs)
    
    @property
    def element_type(self):
        ''' the element HTML type: div, form, etc'''
        return self._element_type
    
    @element_type.setter
    def element_type(self,element_type):
        self._element_type = element_type
        return self.element.tag_name == self.element_type  # allows other tag, caller should check
    
    @property 
    def text(self):        
        return self.element.text    
    
    
class WebElementById(WebElementHtmlBase):
            
    def __init__(self,*args,**kwargs):
                
        super(WebElementById,self).__init__(*args,**kwargs)
        if kwargs.has_key('element_id'):
            self.element_id = kwargs['element_id']
        
    @property
    def element_id(self):
        ''' the element html id'''
        return self._element_id
    @element_id.setter
    def element_id(self,element_id):
        self._element_id = element_id
        self.element = self.wrapper.get_html_element_by_id(element_id)
        
        
class WebElementByClass(WebElementHtmlBase):
    """ returns the first element with the class"""
            
    def __init__(self,*args,**kwargs):
        
        _element_class = None
                
        super(WebElementByClass,self).__init__(*args,**kwargs)        
        if kwargs.has_key('class'):
            self.element_class = kwargs['class']
    
    @property
    def element_class(self):
        return self._element_class
    @element_class.setter
    def element_class(self,element_class):
        self._element_class = element_class
        self.element = self.html_element.get_html_element_by_class(self.element_class)
        
        
class WebElementByXPath(WebElementHtmlBase):


    _element_xpath = None
    xpath_template = ""

    def __init__(self,*args,**kwargs):

        super(WebElementByXPath,self).__init__(*args,**kwargs)        
        if kwargs.has_key('xpath'):
            self.element_xpath = kwargs['xpath']

    @property
    def element_xpath(self):
        return self._element_xpath
    @element_xpath.setter
    def element_xpath(self,element_xpath):
        self._element_xpath = element_xpath
        self.element = self.wrapper.get_html_element_by_xpath(self.element_xpath)
        
    def new_element(self,xpath):
        """get new child element based on the relative xpath to the element xpath"""
        
        new_element = self.__class__.__new__(self.__class__)
        new_element.__init__(browser=self.browser)
        new_element.element_xpath = self.element_xpath + xpath
        return new_element