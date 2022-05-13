from django.urls import path, include, re_path
from django.contrib import admin
from rest_framework.routers import SimpleRouter
from django.contrib.staticfiles.views import serve as serve_static

router = SimpleRouter()


def _static_butler(request, path, **kwargs):
    """
    It's slow but for admin use only it's sufficient
    """
    return serve_static(request, path, insecure=True, **kwargs)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),

    # the 'api-root' from django rest-frameworks default router
    # http://www.django-rest-framework.org/api-guide/routers/#defaultrouter

    re_path(r'static/(.+)$', _static_butler)

]
