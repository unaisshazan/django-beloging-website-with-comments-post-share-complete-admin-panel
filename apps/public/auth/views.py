from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse,reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import generic
from site_repo.cache.API import clear_user_cache
from . import forms


from site_repo.lang import forms_public as lang_forms_public
from . import helpers

def demo_account(request):
    
    user = authenticate(username=settings.DEMO_USER1['username'],
                        password=settings.DEMO_USER1['password'])
    login(request, user)
    return HttpResponseRedirect(reverse("expenses:monthly_all",kwargs={'year':2016,'month':1}))

def password_reset_view(request):
    
    template_name = 'public/auth/password_reset_form.html'
    
    user = None
    if request.method == "POST":
        form = forms.PasswordResetForm(request.POST)
        if form.is_valid():
            try:
                user = User.objects.get(username=form.cleaned_data['username_or_email'])
            except:
                try:
                    user = User.objects.filter(email=form.cleaned_data['username_or_email'])[0]
                except:
                    pass ## no info if user was found or not
            
            if user != None:
                protocol = "https://%s" if request.is_secure() else "http://%s"
                helpers.send_reset_password_mail_to_user(user,protocol%request.get_host())
                
            messages.add_message(request,messages.SUCCESS,lang_forms_public.reset_password_link_sent)
            return HttpResponseRedirect(reverse("home_page"))
    else:
        # method is GET
        form = forms.PasswordResetForm()
        context = {'form':form}
        return render(request,template_name,context)
                
                
    
    

class SignUpView(generic.edit.FormView):
    
    form_class = forms.SignupForm
    template_name = 'public/auth/signup.html'
    success_url = reverse_lazy("expenses:main_redirect")
    
    
    def form_valid(self, form):
        
        user = form.save()
        login(self.request,user)
        return super(SignUpView,self).form_valid(form)
    
    
class LoginView(generic.edit.FormView):
    
    form_class = AuthenticationForm
    template_name = 'public/auth/login.html'
    success_url = reverse_lazy("expenses:main_redirect")
    
    def form_valid(self, form):
        
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(self.request, user)
            return super(LoginView, self).form_valid(form)
        else:
            return self.form_invalid(form)   
        

def logout_user(request):
    
    clear_user_cache(request.user)
    logout(request)
    return HttpResponseRedirect("/")
    
    
    