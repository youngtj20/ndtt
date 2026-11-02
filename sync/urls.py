from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^page/$', views.index),
    url(r'^confirm/center/$', views.identify_center),
    url(r'^local/online/$', views.sync_local_to_online),
    url(r'^online/local/$', views.sync_online_to_local),
    url(r'^perform/online/sync/$', views.do_remote_sync),
    url(r'^perform/local/sync/$', views.get_remote_data),
    url(r'^get/files/$', views.getfiles),
    url(r'^memorize/$', views.memorize),
    ]