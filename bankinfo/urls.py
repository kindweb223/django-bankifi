from django.conf.urls import url

from .views import BanksView, ProductsView

urlpatterns = [
    url(r'^$', BanksView.as_view(), name='banks'),
    url(r'^(?P<bid>.*--\w+)/products$', ProductsView.as_view(), name='products'),
]