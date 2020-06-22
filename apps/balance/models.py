from collections import namedtuple
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from ..accounts.models import Account
from ..expenses.models import Expense

from site_repo.django_add.validators import verify_month_int,verify_month_is_before_this_month
from ...utils.db import run_sql
from .sql import of_year,of_month, sort_clause


class BalanceAggregateManager(models.Manager):
    
    def _get_recs(self,user,year,approved,month=None):
        
        divorcee_id = 0 if user.divorcee == None else user.divorcee.id
        args = [user.account.id,year,year,
                user.id,year,divorcee_id]
        approved_clause={'all':"",'yes':" AND is_approved=1 ",'no': " AND is_approved=0 "}[approved]
       
        if month != None:
            sql = of_month
            args.append(month)
        else:
            sql = of_year + sort_clause
        recs = run_sql(sql.format(approved_clause=approved_clause),*args)
        Lresults = []
        for rec in recs:
            D = {'month_of_balance':rec[0],
                 'year_of_balance':year,
                 'user':user,
                 'user_sum':rec[3],
                 'divorcee_participate':rec[4],
                 'divorcee':user.divorcee,
                 'divorcee_sum':rec[7],
                 'user_participate':rec[8]
                 }
            D['user_sum'] = 0 if D['user_sum'] == None else D['user_sum']
            D['divorcee_participate'] = 0 if D['divorcee_participate'] == None else D['divorcee_participate']
            D['divorcee_sum'] = 0 if D['divorcee_sum'] == None else D['divorcee_sum']
            D['user_participate'] = 0 if D['user_participate'] == None else D['user_participate']
            D['user_net'] = D['user_sum'] + D['user_participate'] - D['divorcee_participate']
            D['divorcee_net'] = D['divorcee_sum'] + D['divorcee_participate'] - D['user_participate']
            D['total'] = D['user_sum'] + D['divorcee_sum']
            Lresults.append(D)
           
 
        q = self.model.objects.filter(year_of_balance=year,account=user.account,
                                     month_of_balance__in=[m['month_of_balance'] for m in Lresults])
        Dq = {balance_obj.month_of_balance:balance_obj for balance_obj in q}
        for Dbalance in Lresults:
            obj = Dq[Dbalance['month_of_balance']]
            Dbalance['balance_object']  = obj
            Dbalance['cleared'] = obj.divorcee1 != None and obj.divorcee2 != None
            
        return Lresults
    
    def by_month(self,user,year,month,approved="all"):
        
        return self._get_recs(user, int(year),approved, int(month))[0]
    
    def by_year(self,user,year,approved="all"):
        
        return self._get_recs(user, int(year),approved)
    
class Objects(models.Manager):
    pass
                        

class MonthlyBalance(models.Model):
    
    class Meta:
            unique_together =('month_of_balance','year_of_balance','account')  
    
    month_of_balance = models.IntegerField(validators=[verify_month_int])
    year_of_balance = models.IntegerField()
    
    account = models.ForeignKey(Account,related_name="months_balanced")
    
    divorcee1 = models.ForeignKey(User,blank=True,null=True,related_name="divorcee1_balance")
    divorcee2 = models.ForeignKey(User,blank=True,null=True,related_name="divorcee2_balance")
    
    is_balanced = models.BooleanField(default=False)
    
    balance_aggregate = BalanceAggregateManager()
    objects = Objects() # not avialable w/o explicit assignment when other manager assigned
    
    def save(self,*args,**kwargs):
        
        if not kwargs.get('force_insert',False):
            # can not balance an account for a month before the month finishes
            verify_month_is_before_this_month(self.year_of_balance,self.month_of_balance)
        
        return super(MonthlyBalance,self).save(*args,**kwargs)
        
        
    
    
    def get_absolute_url(self):
        
        return reverse("balance:details",kwargs={'year':self.year_of_balance,
                                                 'month':self.month_of_balance})
    
    def divorcee_cleared_month(self,user):
        
        if user != None:
            return self.divorcee1 == user or self.divorcee2 == user
        else:
            return False
        
    def calcs(self,user):
        a = self.account
        divorcee1_sum = expenses.filter(month_balanced=self.month_of_balance,
                                   year_balanced=self.year_of_balance,
                                   owner=a.divorcee1).aggregate(Sum('expense_sum'),)
    
    
@receiver(post_save,sender=Expense)
def first_expense_for_month(*args,**kwargs):
    
    if not kwargs['created']:
        return
    
    expense = kwargs['instance']
    Dcriteria = {'month_of_balance':expense.month_balanced,
                 'year_of_balance':expense.year_balanced,
                 'account':expense.account}
    try:
        m = MonthlyBalance.objects.get(**Dcriteria)
    except ObjectDoesNotExist:        
        m = MonthlyBalance(**Dcriteria)
        m.save(force_insert=True)