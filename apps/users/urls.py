from django.conf.urls import url
from django.contrib.sessions.middleware import SessionMiddleware

from .views import IndexView,LoginView,LogoutView,RegisterView,ActiveUserView,ForgetView,PasswordResetView,ModifyPwdView

urlpatterns = [
    url(r'^register/$',RegisterView.as_view(),name='register'),
    url(r'^login/$',LoginView.as_view(),name='login'),
    url(r'^logout/$',LogoutView.as_view(),name='logout'),
    url(r'^forget/$',ForgetView.as_view(),name='forget'),
    url(r'^reset_password/(?P<passwordreset_code>\w+)',PasswordResetView.as_view(),name='password_reset'),
    url(r'^modify_password/$',ModifyPwdView.as_view(),name='modify_password'),
    url(r'^active/(?P<active_code>\w+)',ActiveUserView.as_view(),name='active'),
]