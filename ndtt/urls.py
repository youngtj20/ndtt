from django.conf.urls import url, include
from django.contrib import admin
from custom.views import index
from . import settings
import os
from django.conf.urls.static import static
from django.views.static import serve


urlpatterns = [
    url(r'^$', include('welcome.urls')),
    url(r'^myadmin/', index),
    url(r'^admin/', admin.site.urls),
    url(r'^ap/', include('custom.urls')),
    url(r'^api/', include('api.urls')),
    url(r'^synchro/', include('sync.urls')),
] # + static(settings.STATIC_URL, document_root=settings.STATIC_URL) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if os.environ.get('APP_ENV', 'DEVELOPMENT') == "PRODUCTION":
    urlpatterns += [
        url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT, 'show_indexes': True}),
        url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    ]

else:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


