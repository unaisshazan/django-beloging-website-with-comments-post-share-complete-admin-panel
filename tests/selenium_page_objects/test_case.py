from django.test import SimpleTestCase
from .driver import SeleniumDriver

class SeleniumWebTestCaseBase(SimpleTestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.driver = SeleniumDriver()
        cls.browser = cls.driver.browser
        super(SeleniumWebTestCaseBase, cls).setUpClass()
        
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super(SeleniumWebTestCaseBase,cls).tearDownClass()
        
    
        
    
        
        
        
        