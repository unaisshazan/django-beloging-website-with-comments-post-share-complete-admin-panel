
from .models import Expense

def multiple_approval(user,Dapproval):
    """ gets {10:True,20:False...} and sets these expenses approval if possible"""
    
    q = Expense.objects.filter(account=user.account,
                            pk__in=Dapproval.keys())
    
    for expense in q:
        expense.is_approved = Dapproval[expense.pk]
        expense.save()
        
        
    return
    
    