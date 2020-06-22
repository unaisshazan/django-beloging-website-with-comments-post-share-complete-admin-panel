from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from selenium import webdriver

Dselenium_defaults = {
    'EXCLUDE_FIELDS': ['csrfmiddlewaretoken'],
    'CHROME_DRIVER': '/home/aviah/my-django-projects/divorce-calcs/lib/chromedriver',# download the correct version https://sites.google.com/a/chromium.org/chromedriver/downloads
    'WEBDRIVER_USE_BROWSER':'Chrome', # 'Firefox', etc
    'SELENIUM_TIMEOUT_PAGE_LOAD':2, # implict wait, the default for page id
    'SELENIUM_TIMEOUT_WEBDRIVER':2, # explicit wait, the default used when init the driver
    'WAIT_FOR_ELEMENT_TIMEOUT':3, # explicit wait, used to adjust specific find element calls
    'DESIRED_CAPABILITIES': "",
    'HOST': '127.0.0.1:8000', # to use the site host settings.ALLOWED_HOSTS[0]
    'USE_HTTPS': False,
    'CHECK_PAGE_ID': True
}


if hasattr (settings, 'SELENIUM'):
    try:
        for k,v in SELENIUM.iteritems():
            Dselenium_defaults[k] = v
    except:
        raise ImproperlyConfigured()
    

EXCLUDE_FIELDS = Dselenium_defaults['EXCLUDE_FIELDS']
CHROME_DRIVER = Dselenium_defaults['CHROME_DRIVER']
WEBDRIVER_USE_BROWSER = Dselenium_defaults['WEBDRIVER_USE_BROWSER']
SELENIUM_TIMEOUT_PAGE_LOAD = Dselenium_defaults['SELENIUM_TIMEOUT_PAGE_LOAD']
SELENIUM_TIMEOUT_WEBDRIVER = Dselenium_defaults['SELENIUM_TIMEOUT_WEBDRIVER']
WAIT_FOR_ELEMENT_TIMEOUT = Dselenium_defaults['WAIT_FOR_ELEMENT_TIMEOUT']
DESIRED_CAPABILITIES  = Dselenium_defaults['DESIRED_CAPABILITIES']
HOST = Dselenium_defaults['HOST']
USE_HTTPS = Dselenium_defaults['USE_HTTPS']
CHECK_PAGE_ID = Dselenium_defaults['CHECK_PAGE_ID']

WEBDRIVERS = {'Firefox':webdriver.Firefox,
              'Chrome':webdriver.Chrome,
              'Ie':webdriver.Ie,
              'Remote':webdriver.Remote,
              'Phantom':webdriver.PhantomJS}
    
