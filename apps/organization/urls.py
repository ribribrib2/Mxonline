from django.conf.urls import url

from .views import OrgView,AddUserAskView,OrgHomeView,OrgCourseView,OrgDescView,OrgTeacherView,TeacherListView,TeacherDetailView,AddFavView
# from .views import PasswordUploadView

urlpatterns = [
    url(r'^org_list/$',OrgView.as_view(),name='org_list'),
    url(r'^add_ask/$',AddUserAskView.as_view(),name='add_ask'),
    url(r'^add/fav/$',AddFavView.as_view(),name='add_fav'),
    url(r'^org_home/(?P<org_id>\d+)$',OrgHomeView.as_view(),name='org_home'),
    url(r'^org_course/(?P<org_id>\d+)$',OrgCourseView.as_view(),name='org_course'),
    url(r'^org_desc/(?P<org_id>\d+)$',OrgDescView.as_view(),name='org_desc'),
    url(r'^org_teacher/(?P<org_id>\d+)$',OrgTeacherView.as_view(),name='org_teacher'),
    url(r'^teacher/list/$',TeacherListView.as_view(),name='teacher_list'),
    url(r'^teacher/detail/(?P<teacher_id>\d+)$',TeacherDetailView.as_view(),name='teacher_detail'),
]
