from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from aigerim.views import *

from ProjectDjango import settings




urlpatterns = [
    path('admin/', admin.site.urls),
    path('captcha/', include('captcha.urls')),
    path('', include('aigerim.urls')),
    path('api/v1/aigerim/', AigerimAPIList.as_view()),
    path('api/v1/aigerim/<int:pk>/', AigerimAPIUpdate.as_view()),
    path('api/v1/aigerimdelete/<int:pk>/', AigerimAPIDestroy.as_view()),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include('debug_toolbar.urls')),
    ] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# handler404 = pageNotFound

# Routers provide an easy way of automatically determining the URL conf.
# router = routers.DefaultRouter()
# router.register(r'aigerim', AigerimViewSet)
# print(router.urls)

# path('api/v1/aigerimlist/', AigerimAPIList.as_view()),
# path('api/v1/aigerimlist/<int:pk>/', AigerimAPIUpdate.as_view()),
# path('api/v1/aigerimdetail/<int:pk>/', AigerimAPIDetailView.as_view()),

# class MyCustomRouter(routers.DefaultRouter):
#     routes = [
#         routers.Route(url=r'^{prefix}$',
#                       mapping={'get': 'list'},
#                       name='{basename}-list',
#                       detail=False,
#                       initkwargs={'suffix': 'list'}),
#         routers.Route(url=r'{prefix}/{lookup}',
#                       mapping={'get': 'retrieve'},
#                       name='{basename}-detail',
#                       detail=True,
#                       initkwargs={'suffix': 'Detail'})
#     ]
#
# router = MyCustomRouter()
# router.register(r'aigerim', AigerimViewSet, basename='aigerim')
# print(router.urls)
# path('api/v1/', include(router.urls)), url turi