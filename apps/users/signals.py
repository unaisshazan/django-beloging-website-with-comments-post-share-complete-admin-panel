from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import pre_save,pre_delete
from django.dispatch import receiver

from ..expenses.models import Expense
from ..balance.models import  MonthlyBalance
from ..accounts.models import Account
from models import UserSettings

Duser_field = {
    Expense:['owner'],
    UserSettings:['user']
}

msg = ["Demo users can not change data"]
class DemoUserReadOnly(Exception):
    pass

@receiver([pre_save,pre_delete])
def demo_users_read_only(sender,**kwargs):
    """ raises exception for user models, and before search post_save"""
    
    if settings.DEBUG and settings.DEBUG_IGNORE_DEMO_ACCOUNTS:
        return
    
    instance = kwargs['instance']
    if sender == User and instance.id in settings.DEMO_USERS:
        if list(kwargs['update_fields']) == ['last_login']:
            return # sign-in
        else:
            raise DemoUserReadOnly(msg)
    
    if sender == Account and instance.id == settings.DEMO_ACCOUNT:
        raise DemoUserReadOnly(msg)
        
    if sender == MonthlyBalance and instance.account_id == settings.DEMO_ACCOUNT:
        raise DemoUserReadOnly(msg)    
        
    if sender in Duser_field.keys():       
        Lfields = Duser_field[sender] 
        for field in Lfields:
            user = getattr(instance, field)
            if user.id in settings.DEMO_USERS:
                raise DemoUserReadOnly(msg)
            
    
    
    
