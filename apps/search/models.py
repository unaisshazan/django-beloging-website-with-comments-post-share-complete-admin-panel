from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models.signals import post_save,post_delete
from django.contrib.auth.models import User
from django.dispatch import receiver

from ...utils.db import run_sql
from ..accounts.models import Account
from ..accounts.API import get_account_by_user
from . import app_settings

class Objects(models.Manager):
    pass


class SearchResultsManager(models.Manager):
    
    def search(self,account,search_query):
        
        if app_settings.AUTO_WILDCARD and app_settings.WILDCARD not in search_query:
            search_query = search_query + app_settings.WILDCARD
            
        recs = run_sql(app_settings.SELECT,account.id,search_query,app_settings.MAX_ENTRIES)
        
        queryset = super(SearchResultsManager,self).get_queryset()
        queryset = queryset.filter(id__in=[r[0] for r in recs])
        
        Lresults = []
        all_models = User.objects.get(pk=1)._meta.apps.all_models
        for item in queryset:
            Ditem = {'name':item.object_name,
                     'object':all_models[item.app_label][item.model_name].objects.get(pk=item.object_pk)}                     
            Lresults.append(Ditem)
        return Lresults
        
       

class SearchItems(models.Model):
    
    class Meta:
        managed = False # uses custom sql migration for full text index  
        db_table = "search_searchitems"    
    
    object_name = models.CharField(max_length=255)
    search_text = models.CharField(max_length=1024)
    app_label = models.CharField(max_length=128)
    model_name = models.CharField(max_length=128)
    object_pk = models.IntegerField()
    object_account_id = models.IntegerField()
    
    items = SearchResultsManager()
    objects = Objects()
    
    
@receiver(post_save)
def save_search_item(*args,**kwargs):
    
    instance = kwargs['instance']
    if not hasattr(instance,'SearchConfig'):
        return
    
    item_name_field = instance.SearchConfig.item_name_field
    search_fields_set = set(instance.SearchConfig.search_fields)
   
    s = search_fields_set.copy()
    s.add(item_name_field)
    if kwargs['update_fields'] != None:
        if len(s.intersection(kwargs['update_fields'])) == 0:
            return

    search_text = ""
    for field in search_fields_set:
        search_text = search_text + getattr(instance,field) + " "
        
    
    account = get_account_by_user(instance.owner)

    item = SearchItems.objects.get_or_create(object_pk=instance.pk,
                                             app_label=instance._meta.app_label,
                                             model_name=instance._meta.model_name,
                                             object_account_id=account.id)[0]
    
    item.object_name = getattr(instance,item_name_field)
    item.search_text = search_text
    item.save()    
   
    return

@receiver(post_delete)
def delete_search_item(*args,**kwargs):
    
    instance = kwargs['instance']
    if not hasattr(instance,'SearchConfig'):
        return
    
    try:
        item = SearchItems.objects.get(object_pk=instance.pk,
                                       app_label=instance._meta.app_label,
                                       model_name=instance._meta.model_name)
        item.delete()
        
    except ObjectDoesNotExist:
        return
    
    
    
    
    

    
       
