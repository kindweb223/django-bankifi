from django.conf.urls import url

from .views import IndexView, AuthorizationView, ApplyView, ThankyouView, PayLoanView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^authorize/$', AuthorizationView.as_view(), name='authorize'),
    url(r'^apply/$', ApplyView.as_view(), name='apply'),
    url(r'^thankyou/$', ThankyouView.as_view(), name='thankyou'),
    url(r'^payloan/$', PayLoanView.as_view(), name='payloan'),
]