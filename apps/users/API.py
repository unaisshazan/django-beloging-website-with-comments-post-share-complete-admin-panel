import datetime
import pickle
from django.contrib.auth import authenticate
from django.contrib.auth.models  import User
from django.core.exceptions import ValidationError
from django.conf import settings
from ...utils.mail import send_mail_to_user
from ...lang import mail as lang_mail

from ...cache.API import clear_user_cache
from ..accounts.models import Account
from ..tasks_queue.API import push_task_to_queue

def register_user(username,email,password,account_code,mail=True):
    
    account = None
    if len(account_code) > 0:
        try:
            account = Account.objects.get(account_code=account_code)
        except:
            # don't create a user that wants to join an account but provided wrong code
            raise ValidationError(message="No account found for this account code. Please verify that you got the correct code")
   
    if settings.DEBUG and settings.DEBUG_ALLOW_NON_UNIQUE_EMAIL:
        pass # allow non unique emails, for testing
    else:
        if User.objects.filter(email=email).exists():
            raise ValidationError(message="Username or email")
        
    User.objects.create_user(username=username,email=email,password=password)
    user = authenticate(username=username,password=password)    
    
    if account != None:
        assert account.divorcee1 != None
        assert account.divorcee2 == None
        account.divorcee2 = user
        user.divorcee = account.divorcee1
        clear_user_cache(account.divorcee1) ## next request will see divorcee2
    else:
        account = Account(divorcee1=user)
        user.divorcee = None
        
    account.save()
    user.account = account
    
    if mail:
        send_mail_to_user(user,**lang_mail.welcome_mail)
    
    return user
    
def require_auth_to_user_settings(request):
    
    assert request.user.is_authenticated()
    
    last_authenticated = request.session.get('last_authenticated',None)
    if last_authenticated == None:
        return True
    
    n = datetime.datetime.now()
    last_authenticated = pickle.loads(last_authenticated)
    delta = n - last_authenticated
    return delta.seconds > settings.AUTH_SECONDS_TO_ACCESS_USER_SETTINGS
    
    
   