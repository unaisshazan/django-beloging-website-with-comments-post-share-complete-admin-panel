from django.shortcuts import render


from django.views import generic



class AboutPublicView(generic.TemplateView):
    
    template_name = "public/info/about.html"
    
    
class TOSPublicView(generic.TemplateView):
    
    template_name = "public/info/tos.html"
    
class PrivacyPolicyView(generic.TemplateView):
    
    template_name = "public/info/privacy.html"
    
    
    
    