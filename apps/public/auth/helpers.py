from django.core.urlresolvers import reverse
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


from site_repo.lang import mail as lang_mail
from site_repo.utils.mail import send_mail_to_user

def get_token(user):
    
    #assert request.user.is_authenticated()
    
    token_generator = PasswordResetTokenGenerator()
    
    token =  token_generator.make_token(user)
    
    return token
    
    
def get_uid(user):
    
    return urlsafe_base64_encode(force_bytes(user.pk))

def get_reset_url(user):
    
    token  = get_token(user)
    uid = get_uid(user)
    return reverse("password_reset_confirm",args=[uid,token])


def send_reset_password_mail_to_user(user,host):
    
    
    url = host + get_reset_url(user)
    email_message = lang_mail.reset_password_request
    email_message['message'] = email_message['message'].format(url=url)
    send_mail_to_user(user,**email_message)
    
    return
    


    
    
    
    


    
    
    