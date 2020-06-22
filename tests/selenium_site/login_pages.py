from ..selenium_page_objects.pages import WebPageBase
from ..selenium_page_objects import elements_base
from ..selenium_page_objects.helpers import element_exists
from . import elements
from . import forms

class LoginPage(WebPageBase):
    """login required """
        
    def __init__(self,*args,**kwargs):
                
        super(LoginPage,self).__init__(*args,**kwargs)
        
    def add_expense(self):
        self.wrapper.get_html_element_by_id("add_expense").click()
        return self.browser
    
    def side_bar_expenses(self):
        self.wrapper.get_html_element_by_id("side_bar_expenses").click()
        return self.browser
    
    def logout(self):
        self.wrapper.get_html_element_by_id("logout").click()
        return self.browser
        
class ExpenseApprovePage(LoginPage):
    
    page_id = "approve_expense"
    
    def __init__(self,*args,**kwargs):
        super(ExpenseApprovePage,self).__init__(*args,**kwargs)
        self.form = forms.ExpenseApproveForm(browser=self.browser)
        
    def approve_yes(self):
        self.form.approve_check(True)
        return self.browser
       
    def approve_no(self):
        self.form.approve_check(False)
        return self.browser
    
    def save(self):
        self.form.submit()
        return self.browser
        
    
  
class ExpenseDeletePage(LoginPage):
    
    page_id = "delete_expense"
    
    def __init__(self,*args,**kwargs):
        super(ExpenseDeletePage,self).__init__(*args,**kwargs)
        self.form = forms.ExpenseDeleteForm(browser=self.browser)
        
    def delete(self):        
        self.form.submit()
        return self.browser
        
    
class ExpenseAddPage(LoginPage):
    
    page_id = "add_expense"
    
    def __init__(self,*args,**kwargs):
    
        super(ExpenseAddPage,self).__init__(*args,**kwargs)
        self.form = forms.ExpenseForm(browser=self.browser)
            
    def save(self):            
        self.form.submit()
        return self.browser    
    

class ExpenseEditPage(LoginPage):
    
    page_id = "edit_expense"
    
    def __init__(self,*args,**kwargs):
        
        super(ExpenseEditPage,self).__init__(*args,**kwargs)
        self.form = forms.ExpenseForm(browser=self.browser)
        
    def save(self):        
        self.form.submit()
        return self.browser
    
class ExpenseDetailsPage(LoginPage):
    
    page_id = "expense_details"
    
    @property
    def model_html(self):
        m = self.wrapper.get_html_element_by_id("model_html")
        return m.text.split('\n')[:-1]
    
    @property
    def approved(self):
        status = self.wrapper.get_html_element_by_id("approval_status").text
        return {"Approved":True,"Pending":False}[status.strip()]
    
    @property
    @element_exists
    def can_edit(self):
        self.wrapper.get_html_element_by_id("edit_expense")
        
    @property
    @element_exists
    def can_delete(self):
            self.wrapper.get_html_element_by_id("delete_expense")
            
    @property
    @element_exists
    def can_approve(self):
        self.wrapper.get_html_element_by_id("approve_expense")
                    
    def edit(self):
        self.wrapper.get_html_element_by_id("edit_expense").click()
        return self.browser
    
    def delete(self):
        self.wrapper.get_html_element_by_id("delete_expense").click()
        return self.browser
    
    def approve(self):
        self.wrapper.get_html_element_by_id("approve_expense").click()
        return self.browser
        
        
    
    
class ExpensesMonthPage(LoginPage):
    
    _expenses = []
    page_id = 'expenses_month'
    
    def __init__(self,*args,**kwargs):

        url = '/expenses/'
        super(ExpensesMonthPage,self).__init__(url=url,*args,**kwargs)
        self._xpath_template = '//*[@id="expenses_table"]/tbody/tr[%s]'
        if kwargs.has_key('expenses'):
            self.expenses = kwargs['expenses']
            
    @property
    def expenses(self):    
        return self._expenses
    
    @expenses.setter
    def expenses(self,expenses_on_page):
        self._expenses = []
        for m in range(2,expenses_on_page+2):
            expense = elements.ExpenseRowElement(browser=self.browser,xpath=self._xpath_template%m)
            self._expenses.append(expense)
            
    
        