import datetime
from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import render,redirect
from django.views import generic


from ...lang import balance as lang_balance
from ...django_add.validators import verify_month_is_before_this_month

from .helpers import clear_month_balance
from .models import MonthlyBalance

class MainBalanceRedirectView(generic.RedirectView):
    
    def get_redirect_url(self):
        
        n = datetime.datetime.today()
        return reverse("balance:year",kwargs={'year':n.year})
        
class ClearMonthBalanceChangedView(generic.DetailView):     
    
    
    def get(self,request,*args,**kwargs):
        
        year = int(self.kwargs['year'])
        month = int(self.kwargs['month'])
        assert verify_month_is_before_this_month(year,month)
        cleared = {'cleared':True,'not-cleared':False}[request.GET['changed-to']]
        balance = clear_month_balance(user=request.user,
                                      month=month,
                                      year=year,
                                      cleared=cleared)
    
        return redirect(balance)  
        
            
        
        

class ClearMonthBalanceView(generic.DetailView):
    
    model = MonthlyBalance
    template_name = "balance/monthly_balance_clear.html"
    context_object_name = 'balance'
    
    def get_object(self):
        
        year = int(self.kwargs['year'])
        month = int(self.kwargs['month'])
        assert verify_month_is_before_this_month(year,month)        
            
        obj = MonthlyBalance.balance_aggregate.by_month(user=self.request.user,
                                                               year=self.kwargs['year'],
                                                               month=self.kwargs['month'],
                                                               approved="yes")
            
           
            
        return obj
        
    def get_context_data(self,*args,**kwargs):
        
        context = super(ClearMonthBalanceView,self).get_context_data(*args,**kwargs)
        
        L = [self.object['balance_object'].divorcee1,self.object['balance_object'].divorcee2]
        me_cleared = lang_balance.cleared if self.request.user in L else lang_balance.not_cleared
        divorcee_cleared = lang_balance.cleared if self.request.user.divorcee in L else lang_balance.not_cleared
        context['user_cleared'] = self.request.user in L
        context['me_cleared'] = me_cleared%self.request.user.username
        if self.request.user.divorcee:
            context['divorcee_cleared'] = divorcee_cleared%self.request.user.divorcee.username 
        else:
            context['divorcee_cleared'] = ""
            
        context["pay"] = self.object['user_participate'] - self.object['divorcee_participate']
        
        return dict(context,**self.kwargs)
        

class YearlyMonthBalanceView(generic.ListView):
    
    template_name = 'balance/monthly_balance_year.html'
    
    def get_queryset(self):
        
        self.approved = self.request.GET.get('approved','all')
        assert self.approved in ['all','yes','no']
        queryset = MonthlyBalance.balance_aggregate.by_year(self.request.user,self.kwargs['year'],self.approved)
        return queryset
    
    def get_context_data(self,*args,**kwargs):
        
        context = super(YearlyMonthBalanceView,self).get_context_data(*args,**kwargs)
        context['select_years'] = settings.YEARS_TO_FILTER_ON_GUI
        context['approved'] =  {'all':'All','yes': 'Approved','no':'Not Approved'}[self.approved]
        return dict(context,**self.kwargs)


class MonthBalanceView(generic.DetailView):
    
    model = MonthlyBalance
    template_name = 'balance/monthly_balance_details.html'
    context_object_name = 'balance'

    def get_object(self):
        
        self.approved = self.request.GET.get('approved','all')
        assert self.approved in ['all','yes','no']        
        object = MonthlyBalance.balance_aggregate.by_month(user=self.request.user,
                                                           year=self.kwargs['year'],
                                                           month=self.kwargs['month'],
                                                           approved=self.approved)
        
        return object
    
    def get_context_data(self,*args,**kwargs):
                    
        context = super(MonthBalanceView,self).get_context_data(*args,**kwargs)
        
        L = [self.object['balance_object'].divorcee1,self.object['balance_object'].divorcee2]
        me_cleared = lang_balance.cleared if self.request.user in L else lang_balance.not_cleared
        divorcee_cleared = lang_balance.cleared if self.request.user.divorcee in L else lang_balance.not_cleared
        context['me_cleared'] = me_cleared%self.request.user.username
        if self.request.user.divorcee:
            context['divorcee_cleared'] = divorcee_cleared%self.request.user.divorcee.username 
        else:
            context['divorcee_cleared'] = ""
       
        context['approved'] =  {'all':'All','yes': 'Approved','no':'Not Approved'}[self.approved]
        year = int(self.kwargs['year'])
        month = int(self.kwargs['month'])
        context['can_clear'] = verify_month_is_before_this_month(year,month,raise_exception=False) 
        
        context["pay"] = self.object['user_participate'] - self.object['divorcee_participate']
             
        return dict(context,**self.kwargs)    
                