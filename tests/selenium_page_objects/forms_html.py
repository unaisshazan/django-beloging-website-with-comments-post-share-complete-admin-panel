from .selenium_settings import EXCLUDE_FIELDS

def is_user_input_field(input_name):
    
    if len(input_name) < 1 or input_name in EXCLUDE_FIELDS:
        return False
    else:
        return True
    
    
def set_html_checkbox(element,check_to=True):
    
    element.click()
    checked = element.get_attribute('checked')
    
    if checked == 'true':
        if check_to == True:
            return
        else:
            element.click()
            return
    else:
        if check_to == True:
            element.click()
            return
        else:
            return
        
        
        
        
    