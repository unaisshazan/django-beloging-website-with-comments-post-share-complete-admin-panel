from django.conf.urls import url

from . import views

#/balance/
urlpatterns = [   
    url(r'^$',views.MainBalanceRedirectView.as_view(),name="main_redirect"),
    url(r'^(?P<year>[0-9]{4})/$',views.YearlyMonthBalanceView.as_view(),name="year"),    
    url(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$',views.MonthBalanceView.as_view(),name="details"),
     url(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/clear/$',views.ClearMonthBalanceView.as_view(),name="clear"),
     url(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/clear/changed/$',views.ClearMonthBalanceChangedView.as_view(),name="clear_changed"),
    
    ]