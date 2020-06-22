from django.conf.urls import url

from . import views

urlpatterns = [
    
    url(r'^$',views.settings_redirect,name="main_settings_redirect"),
    url(r'^my/$',views.UserSettingsView.as_view(),name="user_settings"),
    url(r'^verify-password/$',views.auth_view,name="auth_user"),
    url(r'^verify-password/ajax$',views.auth_ajax,name="auth_user_ajax"),
    
    ]