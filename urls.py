"""site_repo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.contrib.staticfiles import views
from django.conf.urls.static import static

from django.contrib.auth import views as django_auth_views

from home.views import HomePageView
from apps.help import views as help_views
from apps.public.auth import views as auth_views
from apps.public.info import views as public_info_views
from apps.search.views import SearchView

urlpatterns = [
    # admin
    url(r'^%s/'%settings.ADMIN_URL, include(admin.site.urls)),
    
    # home
    url(r'^$', HomePageView.as_view(), name='home_page'),
    
    # auth
    url(r'^demo/$', auth_views.demo_account, name='demo_account'),
    url(r'^sign-up/$', auth_views.SignUpView.as_view(), name='sign_up_simple'),
    url(r'^login/$', auth_views.LoginView.as_view(), name='login_simple'),
    url(r'^logout/$', auth_views.logout_user, name='logout_simple'),
    url(r'^reset-password/$',auth_views.password_reset_view,name="reset_password"),    
    
    # django auth
    url(r'^reset-password/done/$', django_auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        django_auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', django_auth_views.password_reset_complete, name='password_reset_complete'),
    
    # app modules
    url(r'^settings/', include('site_repo.apps.users.urls',namespace='users')),
    url(r'^expenses/', include('site_repo.apps.expenses.urls',namespace='expenses')),
    url(r'^balance/', include('site_repo.apps.balance.urls',namespace='balance')),   
    url(r'^search/$',SearchView.as_view(),name='search_view'),
    
    url(r'^how-to/$',help_views.IntroView.as_view(),name='intro'),
    
    # public info
    url(r'^about/$',public_info_views.AboutPublicView.as_view(),name="about_public"),
    url(r'^terms-of-service/$',public_info_views.TOSPublicView.as_view(),name="tos_public"),
    url(r'^privacy/$',public_info_views.PrivacyPolicyView.as_view(),name="privacy_policy_public")
]

if settings.DEBUG:
    urlpatterns += [url(r'^static/(?P<path>.*)$', views.serve),]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
    
    
