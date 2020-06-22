from .models import Account

def get_account_by_user(user):
    
    try:
        return Account.objects.get(divorcee1_id=user.id)
    except:
        return Account.objects.get(divorcee2_id=user.id)
    
def get_divorcee_by_account(account,user):
    """ request.user get an account attribute in a middleware, 
    so if caller already has an account, saves repeating database query to get it"""
    
    if account.divorcee1 == user:
        return account.divorcee2
    else:
        return account.divorcee1
    

    