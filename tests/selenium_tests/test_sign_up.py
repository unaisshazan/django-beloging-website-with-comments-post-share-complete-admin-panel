import os
import unittest
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "site_repo.settings")
os.environ["DJANGO_SETTINGS_MODULE"] = "site_repo.settings"   

from site_repo.tests.selenium_site.test_case import SeleniumWebTestCaseWithData
from site_repo.tests.selenium_page_objects.helpers import custom_test_sort
from site_repo.tests.selenium_page_objects.exceptions import NoSuchElementException

from site_repo.tests.load_data import data1
from site_repo.tests.selenium_site import login_pages,public_pages,actions

from site_repo.apps.accounts.models import Account

class SignUpTest(SeleniumWebTestCaseWithData):

    initial_users = data1.Lusers
    initial_expenses = data1.Dexpenses     

    def test_sign_up_existing_account(self):

        home_page= public_pages.HomePage(browser=self.browser)
        sign_up_page = public_pages.SignUpPage(browser=home_page.sign_up())
        account_code  = Account.objects.get(pk=1).account_code
        Dmap = {'username':'Sue','password':'abc123','email':'sue@example.com','account_code':account_code}
        sign_up_page.form.set_input_text(Dmap,clear_form=False)
        exp_month = login_pages.ExpensesMonthPage(browser=sign_up_page.sign_up(),expenses=2)
        home_page = public_pages.HomePage(browser=exp_month.logout())

    def test_sign_up_new_account(self):

        home_page= public_pages.HomePage(browser=self.browser)
        sign_up_page = public_pages.SignUpPage(browser=home_page.sign_up())
        Dmap = {'username':'Tom','password':'passxyz','email':'tom@example.com'}
        sign_up_page.form.set_input_text(Dmap,clear_form=False)
        exp_month = login_pages.ExpensesMonthPage(browser=sign_up_page.sign_up())
        with self.assertRaises (NoSuchElementException):
            exp_month.expenses = 1
        home_page = public_pages.HomePage(browser=exp_month.logout())

    def test_login_new_sign_up(self):
        
        action = actions.SignInHomePageAction(self.browser)
        exp_month = login_pages.ExpensesMonthPage(browser=action.run(username='Sue',password='abc123'))
        browser = action.run(browser=exp_month.logout(),username='Tom',password='passxyz')
        exp_month = login_pages.ExpensesMonthPage(browser=browser)
        exp_month.logout()


if __name__ == '__main__':     
    from site_repo.tests.selenium_site.helpers import set_env
    set_env()
    Ltests = ['test_sign_up_existing_account','test_sign_up_new_account','test_login_new_sign_up']
    unittest.TestLoader.sortTestMethodsUsing = custom_test_sort(Ltests)
    unittest.main()