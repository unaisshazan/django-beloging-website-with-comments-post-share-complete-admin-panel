from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException,InvalidElementStateException

class NonUniqueHtmlElementId(Exception):
    def __init__(self,args=None):
        self.args = args

class BrowserError(Exception):
    def __init__(self,args=None):
        self.args = args

class ElementStateExcpetion(Exception):
    def __init__(self,args=None):
        self.args = args

class ActionFailed(Exception):
    def __init__(self,args=None):
        self.args = args
        
class NoActionMethod(Exception):
    def __init__(self,args=None):
        self.args = args