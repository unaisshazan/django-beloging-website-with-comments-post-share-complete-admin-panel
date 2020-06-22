import datetime
import pickle
import json
from django.conf import settings
from django.contrib.auth import update_session_auth_hash,authenticate
from django.core.urlresolvers import reverse,reverse_lazy
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.views import generic

from . import API
from . import forms


def settings_redirect(request):
    
    if API.require_auth_to_user_settings(request):
        url = reverse("users:auth_user")
    else:
        url = reverse("users:user_settings")
        
    return redirect(url)

def auth_view(request):
    
    return render(request,"users/auth_user.html")
    
def auth_ajax(request):
    
    form = forms.PasswordForm(request.POST)
    if form.is_valid():
        u = authenticate(username=request.user.username,
                         password=form.cleaned_data['password'])
        if u != None:
            request.session['last_authenticated'] = pickle.dumps(datetime.datetime.now())
        response = {'password':'success'} if u != None else {'password':'fail'}
    else:
        response = {'password':'fail'}
        
    return HttpResponse(json.dumps(response), content_type="application/json")
        

class UserSettingsView(generic.FormView):
    
    template_name = "users/user_settings.html"
    form_class = forms.UserSettingsForm
    success_url = reverse_lazy("expenses:main_redirect")
    
    def get(self,request,*args,**kwargs):
        
        if API.require_auth_to_user_settings(self.request):
            return redirect((reverse("users:auth_user")))
        return super(UserSettingsView,self).get(request,*args,**kwargs)
    
    def get_form_kwargs(self,*args,**kwargs):
        
        kwargs = super(UserSettingsView,self).get_form_kwargs(*args,**kwargs)
        kwargs['label_suffix'] = ""
        return kwargs
        
    def get_initial(self,*args,**kwargs):
        
        user = self.request.user
        self.initial = {'send_mail_when_divorcee_approve':user.settings.send_mail_when_divorcee_approve,
                        'send_mail_when_divorcee_balance':user.settings.send_mail_when_divorcee_balance,
                        'base_divorcee_participate':user.settings.base_divorcee_participate,
                        'user_email':self.request.user.email}
    
        return super(UserSettingsView,self).get_initial() 
    
    
    def form_valid(self, form):
        
        password_changed = form.save(self.request.user)
        if password_changed:
            update_session_auth_hash(self.request,self.request.user)
        
        return super(UserSettingsView,self).form_valid(form)
    
    
               
               
    
