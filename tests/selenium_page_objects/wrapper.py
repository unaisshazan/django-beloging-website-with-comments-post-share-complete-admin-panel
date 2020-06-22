from .exceptions import NonUniqueHtmlElementId
from .helpers import poll_dom
from .selenium_settings import WAIT_FOR_ELEMENT_TIMEOUT

class SeleniumWrapper(object):
    
    browser = None
    
    def __init__(self,browser):
        
        self.browser = browser

    def get_html_element_by_id(self,element_id,wait=False,timeout=WAIT_FOR_ELEMENT_TIMEOUT):
    
        func = self.browser.find_elements_by_id
        if not wait:
            Lelements = func(element_id)
        else:
            Lelements = poll_dom(func,element_id,timeout)
    
        if len(Lelements) > 1:
            raise NonUniqueHtmlElementId (['id %s repeates %s times on page'%(element_id,len(Lelements))])
    
        return Lelements[0] ## no element will raise exception
    
    def get_html_element_by_link_text(self,link_text,wait=False,
                                      timeout=WAIT_FOR_ELEMENT_TIMEOUT,all=False,partial_text=True):
        if partial_text:
            func = self.browser.find_elements_by_partial_link_text
        else:
            func = self.browser.find_elements_by_link_text
    
        if not wait:
            Lelements = func(link_text)
        else:
            Lelements = poll_dom(func,link_text,timeout)
    
        if all:
            return Lelements
    
        return Lelements[0] ## no element will raise exception    
    
    
    
    def get_html_element_by_class(self,class_name,wait=False,timeout=WAIT_FOR_ELEMENT_TIMEOUT,all=False):
    
        func = self.browser.find_elements_by_class_name
        if not wait:
            Lelements = func(class_name)
        else:
            Lelements = poll_dom(func,class_name,timeout)
    
        if all:
            return Lelements
    
        return Lelements[0] ## no element will raise exception    
    
    
    
    def get_html_elements_by_css(self,css,wait=False,timeout=WAIT_FOR_ELEMENT_TIMEOUT):
    
        func = self.browser.find_element_by_css_selector
        if not wait:
            Lelements = func(css)
        else:
            Lelements = poll_dom(func,css,timeout)
    
        return Lelements
    
    
    def get_html_element_by_xpath(self,xpath,wait=False,timeout=WAIT_FOR_ELEMENT_TIMEOUT):
    
        func = self.browser.find_element_by_xpath
        if not wait:
            element = func(xpath)
        else:
            element = poll_dom(func,xpath,timeout)
    
        return element