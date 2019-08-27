
""" Django Application URL to view mappings for Demo APIs """

# Import Django modules
from django.conf.urls import url, include
from django.contrib.auth.models import User
# Import django-rest-framework-swagger modules

from rest_framework import routers, serializers, viewsets
from rest_framework.schemas import get_schema_view
from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer
from rest_framework_swagger.views import get_swagger_view

# Import views
from .views import (
        ForecastAPIView,
    )

# Setup routers and set trailing_slash=False for this to work with WSO2
router = routers.DefaultRouter(trailing_slash=False)
# router.register(r'forecast', ForecastAPIView,)
# Setup Swagger schema (requires testing)
schema_view = get_schema_view(title='Bankifi RBS API', renderer_classes=[OpenAPIRenderer, SwaggerUIRenderer])

# Map API urls to views
urlpatterns = [
    url(r'^$', schema_view, name="docs"),
    url(r'^', include(router.urls)),
    url(r'^forecast/(?P<pk>[\w\-]+)/$', ForecastAPIView.as_view(), name='forecast'), # /api/cashflow/forecast
]