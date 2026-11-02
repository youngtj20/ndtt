from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index')
    # url(r'inspect/login$', views.index, name='index'),
]