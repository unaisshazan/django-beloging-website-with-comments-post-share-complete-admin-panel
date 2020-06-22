from site_repo.tests.selenium_page_objects.test_case import SeleniumWebTestCaseBase
from site_repo.tests.load_data import helpers


class SeleniumWebTestCaseWithData(SeleniumWebTestCaseBase):
    
    initial_users = None
    initial_expenses = None
    send_emails = False
    
    @classmethod
    def setUpTestData(cls):
        helpers.add_users(cls.initial_users,cls.send_emails)
        helpers.add_expenses(cls.initial_expenses)
        
    @classmethod
    def setUpClass(cls):
        super(SeleniumWebTestCaseWithData,cls).setUpClass()
        cls.setUpTestData()
        
        
        
        
        
        
        
        
    
    