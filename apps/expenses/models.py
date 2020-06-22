from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator,MaxValueValidator
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify

from site_repo.django_add.validators import verify_month_int

from ..accounts.models import Account
from ..accounts.API import get_account_by_user

Lmonths = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
MONTHS_CHOICES = zip(range(1,13),Lmonths)
YEARS_CHOICES = zip(settings.YEARS_TO_FILTER_ON_GUI,settings.YEARS_TO_FILTER_ON_GUI,)

class MonthlyExpensesManager(models.Manager):
    
    def by_month(self,month,year):
        
        queryset = super(MonthlyExpensesManager,self).get_queryset()
        return queryset.filter(month_balanced=month,year_balanced=year)
    
class Objects(models.Manager):
    pass
    


class Expense(models.Model):
    
    class SearchConfig:
        item_name_field = 'desc'
        search_fields = ['place_of_purchase','notes']

    date_entered = models.DateTimeField(auto_now_add=True, 
                                        verbose_name="Entered On")
    date_purchased = models.DateField(verbose_name="Date of Purchase")
    month_balanced = models.IntegerField(validators=[verify_month_int],verbose_name="Balance on month",choices=MONTHS_CHOICES)
    year_balanced = models.IntegerField(verbose_name="Balance on year",choices=YEARS_CHOICES)

    owner = models.ForeignKey(User,related_name='expenses',verbose_name="Purchased by")
    account = models.ForeignKey(Account,related_name='expenses',blank=True,null=True)

    expense_sum = models.FloatField(verbose_name="Cost")
    expense_divorcee_participate = models.IntegerField(validators=[MinValueValidator(0),
                                                                MaxValueValidator(100)],verbose_name="Divorcee participate %")
                                                                   
    desc = models.CharField(max_length=512,verbose_name="Description")
    slug = models.SlugField(max_length=128,blank=True)
    place_of_purchase = models.CharField(max_length=512,verbose_name="Place of purchase")
    notes = models.CharField(max_length=1024,blank=True,verbose_name="Notes")
    is_approved = models.BooleanField(default=False,verbose_name="Approved?")

    monthly_expenses = MonthlyExpensesManager()
    objects = Objects() # not avialable w/o explicit assignment when other manager assigned
    

    def get_absolute_url(self):
        
        return reverse('expenses:details',args=[str(self.pk),self.slug])
    
    def get_edit_url(self):
            
            return reverse('expenses:edit',args=[str(self.pk),self.slug])
        
    def get_delete_url(self):
                
                return reverse('expenses:delete',args=[str(self.pk),self.slug])    
        
    def get_approve_url(self):
            
            return reverse('expenses:approve',args=[str(self.pk),self.slug])
        
    def get_change_month_balance_url(self):
        
        return reverse('expenses:change_month_balance',args=[str(self.pk),self.slug])

    def save(self,*args,**kwargs):

        self.slug = slugify(self.desc)
        try:
            self.account = self.owner.account
        except:
            self.account = get_account_by_user(self.owner)
        if not self.can_update():
            # pass when loading search items from script
            raise ValidationError(message="Account is balanced for this month, can't add or update expenses")        
        
        super(Expense,self).save(*args,**kwargs)
        
    def delete(self,*args,**kwargs):
        
        if not self.can_update():
            return ValidationError(message="Try to delete locked expense")
        
        if kwargs['user'] != self.owner:
            return ValidationError(message="Not allowed to delete this expense")
        
        return super(Expense,self).delete()
            
        
    def can_update(self):
        
        return not (self.account.locked_expenses(month=self.month_balanced,
                                               year=self.year_balanced))



