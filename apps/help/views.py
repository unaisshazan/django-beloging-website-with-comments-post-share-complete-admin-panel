from django.shortcuts import render

from django.views import generic


class IntroView(generic.TemplateView):
    
    template_name = "help/intro.html"
