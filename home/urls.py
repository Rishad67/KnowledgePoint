#Local urls
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.homePage, name='home_page'),
]
urlpatterns += [ 
    url(r'^user/create/$', views.UserCreate.as_view(), name='user_create'), 
    url(r'^profile/(?P<pk>\d+)/update/$', views.ProfileUpdate.as_view(), name='profile_update'),
    url(r'^user/(?P<pk>\d+)$', views.UserDetailView.as_view(), name='user_detail'),
    url(r'^index/', views.indexPage, name='index_page'),

]
