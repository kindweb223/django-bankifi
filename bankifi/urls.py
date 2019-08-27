"""redbank URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static

from rest_framework.documentation import include_docs_urls

from .views import index


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', index, name='index'),
    url(r'^branch/', include('branch.urls', namespace="branch")),
    url(r'^oauth/', include('obp_oauth.urls', namespace="oauth")),
    url(r'^bankxero/', include('bankxero.urls', namespace="bankxero")),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^bankinfo/', include('bankinfo.urls', namespace="bankinfo")),
    url(r'^api/cashflow/', include('cashflow.api.urls', namespace="cashflow-api")),
    url(r'^cashflow/', include('cashflow.urls', namespace="cashflow")),
    url(r'^nordea/', include('nordea.urls', namespace="nordea")),
    url(r'^api/nordea/', include('nordea.api.urls', namespace="nordea-api")),
    url(r'^rbs/', include('rbs.urls', namespace="rbs")),
    url(r'^aggregate/', include('aggregate.urls', namespace="aggregate")),
    url(r'^api/aggregate/', include('aggregate.api.urls', namespace="aggregate-api")),
    # url(r'^api/aggregate/', include('aggregate.api.urls', namespace="aggregate-api")),
    url(r'^api/rbs/', include('rbs.api.urls', namespace="rbs-api")),
    url(r'^api-auth/', include('rest_framework.urls', namespace="rest_framework")),
    url(r'^docs/', include_docs_urls(title='Bankifi API')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

