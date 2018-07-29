from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/submit$', views.submit, name='submit'),
    url(r'^login/all_users$', views.all_users, name='all_users'),
    url(r'^login/account$', views.account, name='account'),
    url(r'^login/logout$', views.logout, name='logout'),
]