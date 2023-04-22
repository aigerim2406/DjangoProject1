from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from aigerim.views import *
from rest_framework import serializers, routers, viewsets
from ProjectDjango import settings
from aigerim.views import AigerimAPIView

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('captcha/', include('captcha.urls')),
    path('', include('aigerim.urls')),
    path('api/v1/aigerimlist/', AigerimAPIView.as_view()),
    path('api/v1/aigerimlist/<int:pk>/', AigerimAPIView.as_view())
    # path('api-auth/',include('rest_framework.urls',namespace='rest_framework'))
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include('debug_toolbar.urls')),
    ] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = pageNotFound
