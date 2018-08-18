from django.conf.urls import url
from django.contrib.sessions.middleware import SessionMiddleware

from .views import IndexView,UserInfoView,ImageUploadView,LoginView,LogoutView,RegisterView,PasswordForgetView,PasswordResetView,EmailVerifyView,ModifyPwdView
# from .views import PasswordUploadView

urlpatterns = [
    url(r'^info/$',UserInfoView.as_view(),name='info'),
    url(r'^image/upload/$',IndexView.as_view(),name='image_upload'),
    url(r'^reset/password/$', IndexView.as_view(), name='reset_password'),
    url(r'^mycourse',IndexView.as_view(),name='mycourse'),
    url(r'^fav/course',IndexView.as_view(),name='fav_course'),
    url(r'^mymessage',IndexView.as_view(),name='mymessage'),

    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^forget-password/$', PasswordForgetView.as_view(), name='forget_password'),
    url(r'^email-verify/(?P<verify_record>\w+)', EmailVerifyView.as_view(), name='email_verify'),
    url(r'^modify-password/$', ModifyPwdView.as_view(), name='modify_password'),
]
