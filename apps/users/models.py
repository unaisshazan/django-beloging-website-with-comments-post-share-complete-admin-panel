from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserSettings(models.Model):
    
    user = models.OneToOneField(User,related_name="settings")
    send_mail_when_divorcee_approve = models.BooleanField(default=False)
    send_mail_when_divorcee_balance = models.BooleanField(default=False)
    base_divorcee_participate = models.IntegerField(default=50)

@receiver(post_save,sender=User)
def new_user_settings(*args,**kwargs):
    
    if not kwargs['created']:
        return
    
    settings = UserSettings(user=kwargs['instance'])
    settings.save()