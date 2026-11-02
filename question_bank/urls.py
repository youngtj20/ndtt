from django.conf.urls import url

from . import views

urlpatterns = [
    # url(r'^faculty/', views.faculty),
    url(r'^$', views.index, name='index')
]