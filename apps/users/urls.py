from django.conf.urls import url
from django.contrib.sessions.middleware import SessionMiddleware

from .views import LoginView,LogoutView,RegisterView,PasswordForgetView,PasswordResetView,EmailVerifyView,ModifyPwdView

urlpatterns = [
    url(r'^register/$',RegisterView.as_view(),name='register'),
    url(r'^login/$',LoginView.as_view(),name='login'),
    url(r'^logout/$',LogoutView.as_view(),name='logout'),
    url(r'^forget-password/$',PasswordForgetView.as_view(),name='forget_password'),
    url(r'^reset-password/$',PasswordResetView.as_view(),name='reset_password'),
    url(r'^email-verify/(?P<verify_record>\w+)',EmailVerifyView.as_view(),name='email_verify'),
    url(r'^modify-password/$',ModifyPwdView.as_view(),name='modify_password'),
]