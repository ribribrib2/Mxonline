from django.conf.urls import url

from .views import CourseListView,CourseDetailView,CourseInfoView,CourseCommentsView,CourseAddCommentsView,CourseVideoPlayView

urlpatterns = [
    url(r'^list/$',CourseListView.as_view(),name='course_list'),
    url(r'^detail/(?P<course_id>\d+)$',CourseDetailView.as_view(),name='course_detail'),

    url(r'info/(?P<course_id>\d+)/', CourseInfoView.as_view(), name="course_info"),
    # 课程评论
    url(r'comment/(?P<course_id>\d+)/', CourseCommentsView.as_view(), name="course_comments"),
    # 添加评论
    url(r'add_comment/', CourseAddCommentsView.as_view(), name="add_comment"),
    # # 课程视频播放页
    url(r'video/(?P<video_id>\d+)/', CourseVideoPlayView.as_view(), name="video_play"),
]

