from django.conf.urls import url
from . import views
app_name = 'home'
urlpatterns=[
    url(r'^$',views.home,name='home'),
    url(r'^map/$',views.mapView,name='mapView'),
    url(r'^maptry/$',views.mapView,name='mapmark'),
    url(r'^graph/$',views.home,name='home'),
    url(r'^books/$', views.book_list, name='book_list'),
    url(r'^books/create$', views.book_create, name='book_create'),
    url(r'^books/(?P<id>\d+)/update$', views.book_update, name='book_update'),
    url(r'^books/(?P<id>\d+)/delete$', views.book_delete, name='book_delete'),

]
