from django.conf.urls import url, include
from django.views.generic.base import RedirectView

from .views import (
    # BranchListView,
    branch,
    )

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    # url(r'^$', BranchListView.as_view(), name='branches'), # /branch
    url(r'^$', branch, name='branchfinder'), # /branch
    # url(r'^(?P<postcode>\w+)$', branch, name='branches'), # /branch/postcode

    # url(r'^create/$', TweetCreateView.as_view(), name='create'),  # /tweet/create/
    # url(r'^(?P<pk>\d+)/delete/$', TweetDeleteView.as_view(), name='delete'),  # /tweet/1/delete/
    # url(r'^(?P<pk>\d+)/$', TweetDetailView.as_view(), name='detail'), # /tweet/1/
    # url(r'^(?P<pk>\d+)/update/$', TweetUpdateView.as_view(), name='update'), # /tweet/1/update/
]

