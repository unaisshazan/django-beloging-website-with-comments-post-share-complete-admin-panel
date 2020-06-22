from django.conf import settings
from django.core.mail import send_mail
from django.core.validators import EmailValidator

from site_repo.apps.tasks_queue.API import push_task_to_queue

def send_mail_to_user(user,subject,message,ignore_no_email=True):
    
    try:
        EmailValidator(user.email)
    except:
        if ignore:
            return
        else:
            raise
     
    if settings.DEBUG and not settings.DEBUG_SEND_EMAIL:
        return 
    push_task_to_queue(send_mail,subject=subject,
          message=message,
          from_email=settings.FROM_EMAIL,
          recipient_list=[user.email])  
    
          
    return