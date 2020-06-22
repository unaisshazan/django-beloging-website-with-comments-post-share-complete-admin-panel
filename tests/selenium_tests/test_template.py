import os
import unittest
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "site_repo.settings")
os.environ["DJANGO_SETTINGS_MODULE"] = "site_repo.settings"   

from site_repo.tests.selenium_site.test_case import SeleniumWebTestCaseWithData
from site_repo.tests.selenium_page_objects.helpers import custom_test_sort

class MyTest(SeleniumWebTestCaseWithData):
    
    initial_users = {}
    initial_expenses = {}       
            
    def test_baz(self):
        self.assertEqual('baz','baz')
        print "test baz"
        
    def test_foo(self):
        self.assertNotEqual('foo','baz')
        print "test foo"
        
        
if __name__ == '__main__':     
    from site_repo.tests.selenium_site.helpers import set_env
    set_env()
    #Ltests = ['test_foo','test_baz']
    #unittest.TestLoader.sortTestMethodsUsing = custom_test_sort(Ltests)
    unittest.main()