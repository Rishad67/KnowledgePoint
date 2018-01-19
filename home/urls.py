#Local urls
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.homePage, name='home_page'),
]
urlpatterns += [ 
    url(r'^user/create/student$', views.UserCreate.as_view(), name='user_create'), 
    url(r'^user/create/instructor$', views.InstructorCreate.as_view(), name='instructor_create'),
    url(r'^user/(?P<pk>\d+)$', views.UserDetailView.as_view(), name='user_detail'),
    url(r'^user/student/$', views.studentPage, name='student_page'),
    url(r'^user/instructor/$', views.instructorPage, name='instructor_page'),
    url(r'^instructor/(?P<pk>\d+)/follow$', views.follow, name='instructor_follow'),
    url(r'^instructor/(?P<pk>\d+)/about$', views.aboutInstructor, name='about_instructor'),
    url(r'^profile/(?P<pk>\d+)/update/$', views.ProfileUpdate.as_view(), name='profile_update'),
    url(r'^course/(?P<pk>\d+)$', views.CourseDetailView.as_view(), name='course_detail'),
    url(r'^course/create/$', views.CourseCreate.as_view(), name='course_create'),
    url(r'^course/(?P<pk>\d+)/update/$', views.CourseUpdate.as_view(), name='course_update'),
    url(r'^course/(?P<pk>\d+)/rating/$', views.incRating, name='course_rating'),
    url(r'^course/(?P<pk>\d+)/register/$', views.registerCourse, name='course_registration'),
    url(r'^course/(?P<pk>\d+)/launch/$', views.launchCourse, name='course_launch'),
    url(r'^course/search/$', views.courseSearch, name='course_search'),
    url(r'^course/$', views.courseList, name='course_list'),
    url(r'^lesson/(?P<pk>\d+)$', views.LessonDetailView.as_view(), name='lesson_detail'),
    url(r'^lesson/create/$', views.LessonCreate.as_view(), name='lesson_create'),
    url(r'^lesson/(?P<pk>\d+)/update/$', views.LessonUpdate.as_view(), name='lesson_update'),
    url(r'^forum/$', views.userForum, name='user_forum'),
    url(r'^post/create$', views.PostCreate.as_view(), name='post_create'),
    url(r'^post/(?P<pk>\d+)/update/$', views.PostUpdate.as_view(), name='post_update'),
    url(r'^post/(?P<pk>\d+)/delete/$', views.deletePost, name='post_delete'),
    url(r'^post/(?P<pk>\d+)/like/$', views.likePost, name='post_like'),
    url(r'^comment/create/(?P<pk>\d+)$', views.commentPost, name='comment_post'),
    url(r'^comment/(?P<pk>\d+)/delete/$', views.deleteComment, name='comment_delete'),
    url(r'^reply/create/(?P<pk>\d+)$', views.replyComment, name='reply_comment'),
    url(r'^reply/(?P<pk>\d+)/delete/$', views.deleteReply, name='reply_delete'),

]
