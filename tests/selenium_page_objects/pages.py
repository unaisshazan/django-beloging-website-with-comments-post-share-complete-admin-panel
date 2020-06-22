import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .driver import SeleniumDriver
from .exceptions import BrowserError
from .helpers import full_url,verify_browser
from . import selenium_settings
from .wrapper import SeleniumWrapper

get_page_id_js_line = "return document.getElementById('page_id').getAttribute('page_id')"

class WebPageBase(object):
    '''base class, always use the specific subclass'''
        
    page_id = None
    check_page_id = selenium_settings.CHECK_PAGE_ID
    forms = {}
    
    def __init__(self,*args,**kwargs):
        
        try:
            browser = kwargs['browser']
            assert verify_browser(browser)
            self.browser = browser
            self.wrapper = SeleniumWrapper(browser)
        except:
            raise BrowserError,(["No Browser"])
        
        if kwargs.has_key("check_page_id"):
            self.check_page_id = kwargs['check_page_id']
        
        if kwargs.has_key('url'):
            self.url = kwargs['url']
        
        self._check_page_id() # set page_id by subclass before super().__init__ 
        

   
    def _check_page_id(self):
        """ each specific page object has a page id hard coded in it's constructor
        add to page: $('body').append("<span id='page_id' page_id='{{page_id}}' style='display:none;'></span>");"""
        
        if not self.check_page_id:
            return
        
        wait = WebDriverWait(self.browser,selenium_settings.SELENIUM_TIMEOUT_PAGE_LOAD)
        page_id_element = wait.until(EC.presence_of_element_located((By.ID,'page_id')))
        browser_page_id = self.browser.execute_script(get_page_id_js_line)
        
        if browser_page_id != self.page_id:
            ## after login driver may get the page_id before login completes and selenium get the prev page id
            ## so give time to profile page to load, and retry
            for i in range(5):
                time.sleep(1)
                browser_page_id = self.browser.execute_script(get_page_id_js_line)
                if browser_page_id == self.page_id:
                    break
                
        assert browser_page_id.strip() == self.page_id
    
    @property
    def url(self):
        ''' the element HTML type: div, form, etc'''
        return self._url
    @url.setter
    def url(self,new_url):
        self._url = full_url(new_url)
        self.browser.get(self._url)
        return self.browser
       

        

     
     
        
        
        
