from site_repo.tests.selenium_page_objects.actions import SeleniumWebActionBase

from . import public_pages
from . import login_pages

class SignInHomePageAction(SeleniumWebActionBase):
    
    def action_sign_in_home_page(self,username,password):
    
        home_page = public_pages.HomePage(browser=self.browser)
        return home_page.sign_in(username,password)
        
class EditFirstExpenseAction(SeleniumWebActionBase):
    
    def action_edit_first_expense(self,expenses):
        
        exp_month = login_pages.ExpensesMonthPage(browser=self.browser,expenses=expenses)
        exp_details = login_pages.ExpenseDetailsPage(browser=exp_month.expenses[0].details())
        exp_edit =  login_pages.ExpenseEditPage(browser=exp_details.edit())
        return exp_edit.browser
        