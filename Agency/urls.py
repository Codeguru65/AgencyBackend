# from django.conf.urls import url
from django.urls import re_path
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static
...

schema_view = get_schema_view(
   openapi.Info(
      title="Agency Framework",
      default_version='v1',
      description="Framework for Agency ",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="info@xarani.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('insurance/', include('apirequests.urls_links')),
    path('auth/', include('authentication.urls')),
    path('commissions/', include('commission.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
