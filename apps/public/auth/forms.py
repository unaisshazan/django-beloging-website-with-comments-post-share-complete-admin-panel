from django import forms
from django.contrib.auth.forms import UserCreationForm

from site_repo.lang import forms_public
from site_repo.apps.users import API as API_USERS

class PasswordResetForm(forms.Form):
    
    username_or_email = forms.CharField(max_length=None, min_length=None)


class SignupForm(forms.Form):
    
    username = forms.CharField(max_length=32)
    password = forms.CharField(max_length=32,widget=forms.PasswordInput)
    email = forms.EmailField()
    account_code = forms.CharField(max_length=36,min_length=36,required=False,
                                   help_text=forms_public.signup_account_code,
                                   label="Account Code (Optional):")
    
        
    def save(self):
           
        user = API_USERS.register_user(username=self.cleaned_data['username'],
                                       email=self.cleaned_data['email'],
                                       password=self.cleaned_data['password'],
                                       account_code=self.cleaned_data['account_code']) 
        
        return user
        
        
        
    
    