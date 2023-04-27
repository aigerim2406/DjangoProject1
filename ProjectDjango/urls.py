from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView, TokenObtainPairView
from aigerim.views import *
from django.views.decorators.cache import cache_page
from django.conf.urls import handler400, handler403, handler404, handler500


from ProjectDjango import settings




urlpatterns = [
    path('admin/', admin.site.urls),
    path('captcha/', include('captcha.urls')),
    path('', include('aigerim.urls')),
    path('api/v1/djan-auth/', include('rest_framework.urls')),
    path('api/v1/aigerim/', AigerimAPIList.as_view()),
    path('api/v1/aigerim/<int:pk>/', AigerimAPIUpdate.as_view()),
    path('api/v1/aigerimdelete/<int:pk>/', AigerimAPIDestroy.as_view()),
    path('api/v1/auth/', include('djoser.urls')),  #new
    re_path(r'^auth/', include('djoser.urls.authtoken')), #new
    path('api/v1/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include('debug_toolbar.urls')),
    ] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler400 = 'aigerim.views.bad_request'
handler403 = 'aigerim.views.permission_denied'
handler404 = 'aigerim.views.page_not_found'
handler500 = 'aigerim.views.server_error'

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

# path('api/v1/auth/', include('djoser.urls')),  #new
# re_path(r'^auth/', include('djoser.urls.authtoken')), #new