import os
import unittest
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "site_repo.settings")
os.environ["DJANGO_SETTINGS_MODULE"] = "site_repo.settings"   

from site_repo.tests.selenium_site.test_case import SeleniumWebTestCaseWithData

from django.contrib.auth import authenticate
from site_repo.tests.load_data import data1
from site_repo.tests.selenium_site import actions
from site_repo.tests.selenium_site.login_pages import ExpensesMonthPage

class SignInTest(SeleniumWebTestCaseWithData):
    
    initial_users = data1.Lusers
    initial_expenses = data1.Dexpenses
    
    def test_authenticate(self):
        user = authenticate(username="john",password="123456")
        self.assertIsNotNone(user)
    
    def test_signin(self):
        action = actions.SignInHomePageAction(browser=self.browser)
        self.browser = action.run(username="john",password="123456")
        exp_month = ExpensesMonthPage(browser=self.browser)
        
        
if __name__ == '__main__':     
    from site_repo.tests.selenium_site.helpers import set_env
    set_env()
    unittest.main()