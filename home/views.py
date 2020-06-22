import logging
from django.conf import settings
from django.contrib import messages
from django.core.cache import cache
from django.shortcuts import render
from site_repo.utils.requests import get_ip

# login
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.views import generic
from ..lang import forms_public as lang_forms_public



main_logger = logging.getLogger('main')

    
class HomePageView(generic.edit.FormView):
    
    form_class = AuthenticationForm
    template_name = 'home_page.html'
    success_url = reverse_lazy("expenses:main_redirect")
    
    def form_valid(self, form):
        
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(self.request, user)
            return super(HomePageView, self).form_valid(form)
        else:  
            return self.form_invalid(form)
        
    def form_invalid(self,form):
           
        messages.add_message(self.request,messages.ERROR,lang_forms_public.sign_in_fail)
        return super(HomePageView,self).form_invalid(form)



def it_works(request):
    
    try:
        template = 'it_works.html'
        
        context = {'page_title':'It Works',
                   'intro':'Hello World!'}    
        
        context['ip'] = get_ip(request)
        context['is_debug'] = settings.DEBUG
        
        # cache
        cache.set('foo','baz')
    
        # logging
        main_logger.info("log msg from home_page to main log, also logs to debug log")
        logging.debug("log msg from home_page to debug log")
        request.session['foo'] = 'baz' # a db interaction
        
        return render(request,template,context)
    
    except:
        
        main_logger.exception("Home page exception")
        raise
    
    
    
