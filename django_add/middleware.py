import logging
import sys
from django.conf import settings
from django.http import Http404,HttpResponseRedirect
from django.core.urlresolvers import reverse
from ..cache.API import get_user_cache,set_user_cache

from ..apps.accounts.API import get_account_by_user,get_divorcee_by_account

class AuthorizedViews(object):
    
    def process_view(self,request,view_func,*arg,**kwargs):
        
        if request.path_info.split('/')[1] == settings.ADMIN_URL:
            return None
        
        if view_func.__module__  in settings.PUBLIC_VIEWS_MODULES:
            return None
        
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse('home_page'))


class LogExceptions(object):
    """logs any unhandled views exceptions, ignores Http404"""

    def process_exception(self,request, exception):
        
        if isinstance(exception, Http404):
            
            return

        logging.getLogger('main').critical(exception,exc_info=sys.exc_info())
        
        return
    
class UserAttribute(object):
    """adds additional useful attributes to auth user object"""
    
    def process_view(self,request,view_func,*args,**kwargs):
 
        if request.user.is_authenticated():
            account,divorcee = None,None            
            try:
                D = get_user_cache(request.user)
                account = D['account']
                divorcee = D['divorcee']
            except:
                account = get_account_by_user(request.user)
                divorcee = get_divorcee_by_account(account,request.user)
                set_user_cache(request.user,{'account':account,'divorcee':divorcee})
            finally:  
                request.user.account = account
                request.user.divorcee = divorcee            
                return None
                

    
    