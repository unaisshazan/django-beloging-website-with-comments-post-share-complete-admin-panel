from . models import MonthlyBalance


def clear_month_balance(user,month,year,cleared):
    
    assert cleared in [True,False] # explicit 
    
    balance = MonthlyBalance.objects.get(account=user.account,
                             month_of_balance=month,
                             year_of_balance=year)
    
    if cleared == True:
        
        if balance.divorcee_cleared_month(user):
            return balance  # no change
        
        if balance.divorcee1 == None:
            balance.divorcee1_id = user.id
        else:
            assert balance.divorcee2 == None ## checked it above
            balance.divorcee2_id = user.id
            
    
    else:
        
        if not balance.divorcee_cleared_month(user):
            return balance# no change  
                
                
        if balance.divorcee1 == user:
            balance.divorcee1 = None
        else:
            assert balance.divorcee2 == user ## checked it above
            balance.divorcee2 = None 
            
    
    balance.save()
    return balance
        
        
        
            
  
        
        
    