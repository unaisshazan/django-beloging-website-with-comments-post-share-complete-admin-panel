import os
import unittest
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "site_repo.settings")
os.environ["DJANGO_SETTINGS_MODULE"] = "site_repo.settings"   

from site_repo.tests.selenium_site.test_case import SeleniumWebTestCaseWithData
from site_repo.tests.selenium_page_objects.helpers import custom_test_sort

from site_repo.tests.load_data import data1,helpers
from site_repo.tests.selenium_site import login_pages,public_pages,actions

from site_repo.apps.accounts.models import Account

class ApproveExpenseTest(SeleniumWebTestCaseWithData):
    
    initial_users = data1.Lusers
    initial_expenses = data1.Dexpenses
    
    @classmethod
    def setUpClass(cls):
        super(ApproveExpenseTest,cls).setUpClass()
        account_code  = Account.objects.get(pk=1).account_code
        helpers.add_users(Lusers=[{'username':'Sue','password':'abc123','email':'sue@example.com','account_code':account_code}])     
        
    def test_approve_expense(self):
        action = actions.SignInHomePageAction(self.browser)
        exp_month = login_pages.ExpensesMonthPage(browser=action.run(username='Sue',password='abc123'),expenses=2)
        exp_details = login_pages.ExpenseDetailsPage(browser=exp_month.expenses[0].details())
        self.assertFalse(exp_details.approved)
        self.assertTrue(exp_details.can_approve)
        self.assertFalse(exp_details.can_edit)
        self.assertFalse(exp_details.can_delete)
        exp_approve = login_pages.ExpenseApprovePage(browser=exp_details.approve())
        exp_approve.approve_yes()
        exp_details = login_pages.ExpenseDetailsPage(browser=exp_approve.save())
        self.assertTrue(exp_details.approved)
        exp_month = login_pages.ExpensesMonthPage(browser=exp_details.side_bar_expenses(),expenses=2)
        self.assertTrue(exp_month.expenses[0].approved)
        exp_month.logout()
        
        
    def test_approved_for_account(self):
        action = actions.SignInHomePageAction(self.browser)
        exp_month = login_pages.ExpensesMonthPage(browser=action.run(username='john',password='123456'),expenses=2)        
        expense = exp_month.expenses[0]
        self.assertTrue(expense.approved)
        
        
if __name__ == '__main__':     
    from site_repo.tests.selenium_site.helpers import set_env
    set_env()
    Ltests = ['test_approve_expense','test_approved_for_account']
    unittest.TestLoader.sortTestMethodsUsing = custom_test_sort(Ltests)
    unittest.main()