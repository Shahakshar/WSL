from django.contrib import admin
from django.urls import path, include

from rest_framework.documentation import include_docs_urls
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import re_path

schema_view = get_schema_view(
   openapi.Info(
      title="File Sharing API",
      default_version='v1',
      description="Manage file upload, transfer, revocation, and history with ownership control.",
      contact=openapi.Contact(email="akdev6298@gmail.com"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/file/', include('uploadFile.urls')),


    # Swagger UI
    re_path(r'^$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # path('docs/', include_docs_urls(title='File Sharing API', permission_classes=[permissions.AllowAny])),
]
