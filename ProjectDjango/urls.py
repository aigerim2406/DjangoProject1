from django.conf.urls.static import static
from django.contrib import admin

from aigerim.views import *
from django.urls import path, include

from ProjectDjango import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('aigerim.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include('debug_toolbar.urls')),
    ] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = pageNotFound
