import time
from selenium.webdriver.common.keys import Keys
from .elements_base import WebElementById,WebElementByClass
from . import exceptions  
from .helpers import verify_browser,is_user_input_field
from .wrapper import SeleniumWrapper

class WebFormBase(object):
    """ base class, not to use directly in scripts """
    
    def __init__(self,*args,**kwargs):
        pass
        
        
    def get_form_element(self):
        
        self.form = self.element
        assert self.form.tag_name.lower() == 'form' #element is the form
        self._get_text_input_elements()        
    
        
    def _get_text_input_elements(self):
        """collects input and textarea elements
        silently ignores elements w/o name attribue
        """
        Linput_elements = self.form.find_elements_by_css_selector('#%s input'%self.element_id)
        Linput_elements.extend(self.form.find_elements_by_css_selector('#%s textarea'%self.element_id))
        self._Dinput_elements = dict((x.get_attribute('name'),x) for x in Linput_elements if is_user_input_field(x.get_attribute('name')))

    def set_input_text(self,Ddata_map,clear_form=True):
        '''Data_map = {"elementID1":"something", "elementID2:"somethingelse"...}'''
        if clear_form:
            self.clear_text_elements()        
        for name,element in self.input_text_elements().iteritems():
            if name in Ddata_map:
                try:
                    element.clear()
                    element.send_keys(Ddata_map[name])
                    element.send_keys(Keys.TAB) 
                except:
                    # possibly check for elements that should not raise an exception
                    raise


    def input_text_elements(self):
        return self._Dinput_elements

    def clear_text_elements(self):
        for input_element in self._Dinput_elements.itervalues():
            try:
                input_element.clear()           
            except exceptions.InvalidElementStateException:
                    time.sleep(3)
                    input_element.clear()          

    def submit(self):

        self.form.find_element_by_css_selector('input[type="submit"]').click()

class WebFormById(WebElementById,WebFormBase):

    def __init__(self,*args,**kwargs):
        
        super(WebFormById,self).__init__(*args,**kwargs)
        self.get_form_element()
        

class WebFormByClass(WebElementByClass,WebFormBase):

    def __init__(self,*args,**kwargs):

        super(WebFormByClass,self).__init__(*args,**kwargs)
        self.get_form_element()
        
    