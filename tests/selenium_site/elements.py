from site_repo.tests.selenium_page_objects import elements_base,exceptions

class ExpenseRowElement(elements_base.WebElementByXPath):
    
    def __init__(self,*args,**kwargs):
        super(ExpenseRowElement,self).__init__(*args,**kwargs)
       
    def details(self):        
        self.element.find_element_by_xpath(self.element_xpath+"/td[1]/a").click()
        return self.browser
    
    @property
    def approved(self):
        
        try:
            approved_value = self.element.find_element_by_xpath(self.element_xpath+"/td[6]/input").get_attribute("checked")
        except exceptions.NoSuchElementException:
            approved_value = self.element.find_element_by_xpath(self.element_xpath+"/td[6]/span").get_attribute("approved")
            
        return approved_value == "true"
    