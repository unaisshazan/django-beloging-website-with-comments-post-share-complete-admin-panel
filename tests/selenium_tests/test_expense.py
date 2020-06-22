import os
import unittest
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "site_repo.settings")
os.environ["DJANGO_SETTINGS_MODULE"] = "site_repo.settings"   

from site_repo.tests.selenium_page_objects.exceptions import NoSuchElementException
from site_repo.tests.selenium_page_objects.helpers import custom_test_sort
from site_repo.tests.selenium_site.test_case import SeleniumWebTestCaseWithData

from site_repo.tests.load_data import data1
from site_repo.tests.selenium_site import actions,helpers
from site_repo.tests.selenium_site import login_pages

class ExpenseTest(SeleniumWebTestCaseWithData):
    
    initial_users = data1.Lusers
    initial_expenses = data1.Dexpenses   
      
    def test_expenses_list(self):
            action = actions.SignInHomePageAction(browser=self.browser)
            self.browser = action.run(username='john',password='123456')
            exp_month = login_pages.ExpensesMonthPage(browser=self.browser,expenses=2)
            self.assertEqual(exp_month.expenses[0].text,
                             helpers.format_today_full('School john 130 50% {today} -'))
            self.assertEqual(exp_month.expenses[1].text,
                                         helpers.format_today_full('Sneakers john 90 50% {today} -'))            
    
    def test_expense_details(self):
        exp_month = login_pages.ExpensesMonthPage(browser=self.browser,expenses=2)
        self.browser = exp_month.expenses[0].details()
        exp_details = login_pages.ExpenseDetailsPage(browser=self.browser)
        Lmodel_html = ['Description School', 'Place of purchase Book Store', 'Purchased by john',
                       helpers.format_today('Date of Purchase {today}'), u'Cost 130.0', u'Divorcee participate % 50', u'Notes']
        self.assertEqual(exp_details.model_html,Lmodel_html)
        self.assertFalse(exp_details.approved)
        self.assertTrue(exp_details.can_edit)
        self.assertTrue(exp_details.can_delete)
        
    def test_edit_expense(self):
        
        action = actions.EditFirstExpenseAction(browser=self.browser)
        exp_edit = login_pages.ExpenseEditPage(browser=action.run(expenses=2))
        exp_edit.form.set_input_text({'desc':'School Books'},clear_form=False)
        exp_details = login_pages.ExpenseDetailsPage(browser=exp_edit.save())
        Lmodel_html = ['Description School Books', 'Place of purchase Book Store', 'Purchased by john',
                               helpers.format_today('Date of Purchase {today}'), u'Cost 130.0', u'Divorcee participate % 50', u'Notes']
        self.assertEqual(exp_details.model_html,Lmodel_html)        
        
    def test_add_expense(self):
        exp_month = login_pages.ExpensesMonthPage(browser=self.browser,expenses=2)
        exp_add = login_pages.ExpenseAddPage(browser=exp_month.add_expense())
        Dinput = {'desc':'Books1','expense_sum':'100','place_of_purchase':'amazon.com','notes':'spare book'}
        exp_add.form.set_input_text(Dinput,clear_form=False)
        exp_details = login_pages.ExpenseDetailsPage(browser=exp_add.save())
        Lmodel_html = ['Description Books1', 'Place of purchase amazon.com', 'Purchased by john',
                                       helpers.format_today('Date of Purchase {today}'), u'Cost 100.0', u'Divorcee participate % 50', u'Notes spare book']  
        self.assertEqual(exp_details.model_html,Lmodel_html)
        exp_month = login_pages.ExpensesMonthPage(browser=exp_details.side_bar_expenses(),expenses=3)
        self.assertEqual(exp_month.expenses[2].text,
                         helpers.format_today_full('Books1 john 100 50% {today} -'))
        
    def test_delete_expense(self):
        exp_month = login_pages.ExpensesMonthPage(browser=self.browser,expenses=3)
        exp_details = login_pages.ExpenseDetailsPage(browser=exp_month.expenses[2].details())
        exp_delete = login_pages.ExpenseDeletePage(browser=exp_details.delete())
        with self.assertRaises (NoSuchElementException):
            exp_month = login_pages.ExpensesMonthPage(browser=exp_delete.delete(),expenses=3)
        
if __name__ == '__main__':     
    from site_repo.tests.selenium_site.helpers import set_env
    set_env()
    Ltests = ['test_expenses_list',
              'test_expense_details',
              'test_edit_expense',
              'test_add_expense',
              'test_delete_expense']
    unittest.TestLoader.sortTestMethodsUsing = custom_test_sort(Ltests)
    unittest.main()