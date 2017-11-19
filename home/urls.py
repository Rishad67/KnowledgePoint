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
    url(r'^user/student', views.studentPage, name='student_page'),
    url(r'^user/instructor', views.instructorPage, name='instructor_page'),
    url(r'^course/(?P<pk>\d+)$', views.CourseDetailView.as_view(), name='course_detail'),
    url(r'^course/create/$', views.CourseCreate.as_view(), name='course_create'),
    url(r'^course/(?P<pk>\d+)/update/$', views.CourseUpdate.as_view(), name='course_update'),
    url(r'^lesson/(?P<pk>\d+)$', views.LessonDetailView.as_view(), name='lesson_detail'),
    url(r'^lesson/create/$', views.LessonCreate.as_view(), name='lesson_create'),
    url(r'^lesson/(?P<pk>\d+)/update/$', views.LessonUpdate.as_view(), name='lesson_update'),
]
