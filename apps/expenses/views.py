import datetime
import json

from django.conf import settings
from django.core.urlresolvers import reverse,reverse_lazy
from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404,redirect
from django.views import generic
from django.views.decorators.http import require_POST

from ...utils.view_utils import PaginationContextMixin,ModelToHtmlMixin

from .helpers import multiple_approval
from .forms import ExpenseOwnerForm,ExpenseApproveForm,ExpenseChangeBalanceMonth
from .models import Expense


expense_views_fields = ['desc','place_of_purchase','owner','date_purchased','expense_sum',
                               'expense_divorcee_participate','notes', 'date_entered']

#@require_POST
def expenses_multiple_approve(request):
    
    try:
        Dapproval  = {}
        for k,v in request.POST.iteritems():
            Dapproval[int(k)] = True if v == "true" else False
        multiple_approval(request.user,Dapproval)
        return HttpResponse(status=200)
    
    except:
        return HttpResponse(status=500)
         
        
    
    


class MainExpensesRedirectView(generic.RedirectView):
    
    def get_redirect_url(self,*arg,**kwargs):
        
        n = datetime.date.today()
        return reverse("expenses:monthly_all",kwargs={'month':n.month,'year':n.year})
        
 

class MonthlyExpensesBaseView(generic.ListView):
    
    model = Expense
    template_name = 'expenses/expenses_month.html'
    
    def get_queryset(self):
        
        return Expense.monthly_expenses.by_month(month=int(self.kwargs['month']),
                                                       year=int(self.kwargs['year'])).filter(account=self.request.user.account)
    
class MonthlyExpensesAllView(MonthlyExpensesBaseView,PaginationContextMixin):
    
    def get_queryset(self):

        self.approved = self.request.GET.get('approved','all')
        assert self.approved in ['all','yes','no']        
        self.by = self.request.GET.get('by','all')
        assert self.approved in ['all','yes','no'] 
        assert self.by in ['all','my','divorcee']
        queryset = super(MonthlyExpensesAllView,self).get_queryset()
        if self.approved != 'all':
            queryset = queryset.filter(is_approved=(self.approved=='yes'))
        if self.by == 'my':
            queryset = queryset.filter(owner=self.request.user)
        elif self.by == 'divorcee':
            queryset = queryset.filter(owner=self.request.user.divorcee)
            
        return queryset.all()

    
    def get_context_data(self,*args,**kwargs):
 
        context = super(MonthlyExpensesAllView,self).get_context_data(*args,**kwargs)
        context['approved'] =  {'all':'All','yes': 'Approved','no':'Not Approved'}[self.approved]
        context['by'] = {'all':'By All','my':'My','divorcee':'Divorcee'}[self.by]
        context['select_years'] = settings.YEARS_TO_FILTER_ON_GUI
        context['select_months'] = range(1,13)
        
        context['approved_url_args'] = 'approved={approved}'.format(approved=self.approved)
        context['by_url_args'] = 'by={by}'.format(by=self.by)
        
        if self.request.user.account.locked_expenses(month=self.kwargs['month'],year=self.kwargs['year']):
            context['locked_expenses'] = True
            context['balance_url'] = self.request.user.account.months_balanced.get(month_of_balance=self.kwargs['month'],
                                               year_of_balance=self.kwargs['year']).get_absolute_url()
        
        
        # pagination
        self.update_pagination_context(context)
       
        return dict(context,**self.kwargs)
    
class MonthlyExpensesMyView(MonthlyExpensesBaseView):
    
    def get_queryset(self):
        
        queryset = super(MonthlyExpensesMyView,self).get_queryset()
        return queryset.filter(owner=self.request.user)
    
class MonthlyExpensesDivorceeView(MonthlyExpensesBaseView):
    
    def get_queryset(self):
        
        queryset = super(MonthlyExpensesDivorceeView,self).get_queryset()
        return queryset.filter(owner=self.request.user.divorcee)
    
    
class ChangeExpenceBalanceMonthView(ModelToHtmlMixin,generic.UpdateView):
    
    template_name = "expenses/expense_change_balance_month.html"
    model = Expense
    model_to_html_fields = expense_views_fields
    context_object_name = 'expense'
    form_class = ExpenseChangeBalanceMonth
      
    
    def get_object(self):
        
        if hasattr(self,"object"):
            return self.object
        
        object = get_object_or_404(Expense,pk=int(self.kwargs['pk']),
                                   account=self.request.user.account)
        
        return object
    
    def get(self,request,*args,**kwargs):
    
        self.object = self.get_object()
    
        if self.object.owner == request.user and not self.object.is_approved:
            # this form is userd only to change balance month for non approved expenses
            # to move the expense to another month, where it could be balanced w/o re-entry
            return super(ChangeExpenceBalanceMonthView,self).get(request,*args,**kwargs) 
        else:
            return redirect(self.object)


class ApproveExpenseView(ModelToHtmlMixin,generic.UpdateView):
    
    template_name = "expenses/expense_approve.html"
    model = Expense
    model_to_html_fields = expense_views_fields
    context_object_name = "expense"
    form_class = ExpenseApproveForm
       
    
    def get_object(self):
        
        if hasattr(self,"object"):
            return self.object
        
        object =  get_object_or_404(Expense,pk=int(self.kwargs['pk']),
                                    account=self.request.user.account)
        return object
    
    def get_form_kwargs(self,*args,**kwargs):
    
        kwargs = super(ApproveExpenseView,self).get_form_kwargs(*args,**kwargs)
        kwargs['label_suffix'] = ""
        return kwargs    
    
    def get(self, request, *args, **kwargs):
        
        self.object = self.get_object()
        if self.object.owner != request.user and  self.object.can_update():
            return super(ApproveExpenseView, self).get(request, *args, **kwargs)
        else:
            return redirect(self.object) 

class EditExpenseView(generic.UpdateView):
    
    template_name = "expenses/expense_edit.html"
    model = Expense
    form_class = ExpenseOwnerForm
    
    def get_object(self):
        
        if hasattr(self,"object"):
            return self.object
        
        object =  get_object_or_404(Expense,pk=int(self.kwargs['pk']),
                                    account=self.request.user.account)
        return object
    
    def get(self, request, *args, **kwargs):
        
        self.object = self.get_object()
        expense = self.object
        if expense.owner == request.user and not(expense.is_approved) and expense.can_update() :
            return super(EditExpenseView, self).get(request, *args, **kwargs)
        else:
            return redirect(self.object)        
        
    
class ExpenseView(ModelToHtmlMixin,generic.DetailView):
    
    template_name = "expenses/expense_details.html"
    context_object_name = "expense"
    
    model_to_html = Expense
    model_to_html_fields = expense_views_fields
    
    def get_object(self):
               
        obj =  get_object_or_404(Expense,pk=int(self.kwargs['pk']),
                                    account=self.request.user.account)
        return obj
    
class DeleteExpenseView(ModelToHtmlMixin,generic.DeleteView):
    
    model = Expense
    model_to_html_fields = expense_views_fields
    template_name = "expenses/expense_delete.html"
    success_url = reverse_lazy("expenses:main_redirect")
    
    def get_object(self,*args,**kwargs):
                   
            obj =  get_object_or_404(Expense,pk=int(self.kwargs['pk']),
                                        owner=self.request.user)
            return obj
        
    def delete(self, request,*args,**kwargs):
        
        self.object = self.get_object()
        self.object.delete(self,user=request.user)
        return redirect(self.get_success_url())
    
    
        
    
class AddExpenseView(generic.CreateView):
    
    model = Expense
    form_class = ExpenseOwnerForm
    template_name = "expenses/expense_add.html"
    
    n = datetime.datetime.now()
    initial = {'date_purchased':n,
               'month_balanced':n.month,
               'year_balanced':n.year
               }    
    
    def get_initial(self,*args,**kwargs):
        
        self.initial['expense_divorcee_participate'] = self.request.user.settings.base_divorcee_participate
        return super(AddExpenseView,self).get_initial(*args,**kwargs)
        
        
    def form_valid(self, form):
        
        self.object = form.save(commit=False)
        self.object.owner = self.request.user        
        return super(AddExpenseView,self).form_valid(form)
        
        
    
     
     