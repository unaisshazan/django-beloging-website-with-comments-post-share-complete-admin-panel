import uuid
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db import models

def default_account_code():
    
    return str(str(uuid.uuid4()))

class Account(models.Model):
    
    divorcee1 = models.ForeignKey(User,related_name="divorcee1_account")
    divorcee2 = models.ForeignKey(User,related_name="divorcee2_account",blank=True,null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    account_code = models.CharField(max_length=36,default=default_account_code)
    
    def locked_expenses(self,month,year):
        
        try:
            balance = self.months_balanced.get(month_of_balance=month,
                                               year_of_balance=year)
        
            return balance.divorcee1 != None or balance.divorcee2 != None
        except ObjectDoesNotExist:
            # First balance for month created after first expense in account for that month is saved
            return False
    