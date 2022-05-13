from django.urls import path, include, re_path
from django.contrib import admin
from rest_framework import permissions
from rest_framework.routers import SimpleRouter
from django.contrib.staticfiles.views import serve as serve_static

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

router = SimpleRouter()

schema_view = get_schema_view(
   openapi.Info(
      title="Family Budget API",
      default_version='v1',
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)



def _static_butler(request, path, **kwargs):
    """
    It's slow but for admin use only it's sufficient
    """
    return serve_static(request, path, insecure=True, **kwargs)


urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/v1/', include([
        path('', include('dj_rest_auth.urls')),
        path('', include('django.contrib.auth.urls')),
        path('registration/', include('dj_rest_auth.registration.urls')),
        path('', include(router.urls))
    ])),

    # the 'api-root' from django rest-frameworks default router
    # http://www.django-rest-framework.org/api-guide/routers/#defaultrouter

    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    re_path(r'static/(.+)$', _static_butler)

]
