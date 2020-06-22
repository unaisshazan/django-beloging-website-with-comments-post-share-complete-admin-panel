from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.views import password_change
from ...lang import forms_login as lang_forms_login

class UserSettingsForm(forms.Form):
    
    send_mail_when_divorcee_approve = forms.BooleanField(label=lang_forms_login.mail_approve,required=False)
    send_mail_when_divorcee_balance = forms.BooleanField(label=lang_forms_login.mail_balance,required=False)
    user_email = forms.EmailField(required=False,label="Email")
    base_divorcee_participate = forms.IntegerField(label=lang_forms_login.base_participate)
    password1 = forms.CharField(required=False,widget=forms.PasswordInput(),label="New Password")                                                                     
    password2 = forms.CharField(required=False,widget=forms.PasswordInput(),label="New Password Again")
    
    def clean(self):
        
        cleaned_data = super(UserSettingsForm,self).clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        
        if (password1 != "" or password2 != "") and (password1 != password2):
                raise forms.ValidationError(message="password_not_match")
        
        return
            
    
    def save(self,user):
        
        password_changed = False
        if self.cleaned_data['password1'] != "" and self.cleaned_data['password1'] != None:
            user.set_password(self.cleaned_data['password1'])
            password_changed = True
                    
        if self.cleaned_data['user_email'] != "" and self.cleaned_data['user_email'] != None:
            user.email = self.cleaned_data['user_email']
            
        user.settings.send_mail_when_divorcee_approve = self.cleaned_data['send_mail_when_divorcee_approve']
        user.settings.send_mail_when_divorcee_balance = self.cleaned_data['send_mail_when_divorcee_balance']
        user.settings.base_divorcee_participate = self.cleaned_data['base_divorcee_participate']
        
        user.save()
        user.settings.save()
        
        return password_change
            
            
class PasswordForm(forms.Form):
    
    password = forms.CharField(max_length=36)
        
        
        
        
        
        
    
    
    
    