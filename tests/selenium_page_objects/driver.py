import os
from selenium import webdriver
from . import selenium_settings

# drivers
# www.chromedriver.storage.googleapis.com/index.html


class SeleniumDriver(object):

    def __init__(self,maximize=True):
        '''all tests must start with a dirver, to set the defaults'''
        if selenium_settings.WEBDRIVER_USE_BROWSER == 'Remote':
            self.browser = webdriver.Remote(desired_capabilities=desired_capabilities,
                                            command_executor=sauce_url)

        elif selenium_settings.WEBDRIVER_USE_BROWSER == 'Chrome' and selenium_settings.CHROME_DRIVER != None:
            self.browser = webdriver.Chrome(executable_path=selenium_settings.CHROME_DRIVER) ##from chromium

        else:
            self.browser = selenium_settings.WEBDRIVERS[selenium_settings.WEBDRIVER_USE_BROWSER]()

        self.browser.implicitly_wait(selenium_settings.SELENIUM_TIMEOUT_WEBDRIVER)
        if maximize:
            self.browser.maximize_window()

        return

    def browser(self):
        return self.browser

    def quit(self):
        self.browser.quit()

        
        
        

