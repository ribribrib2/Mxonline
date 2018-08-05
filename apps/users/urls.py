from django.conf.urls import url
from django.contrib.sessions.middleware import SessionMiddleware

from .views import index,LoginView,RegisterView,ActiveUserView,ForgetView,PasswordResetView

urlpatterns = [
    url(r'^login/$',LoginView.as_view(),name='login'),
    url(r'^register/$',RegisterView.as_view(),name='register'),
    url(r'^forget/$',ForgetView.as_view(),name='forget'),
    url(r'^reset_password/(?P<passwordreset_code>\w+)',PasswordResetView.as_view(),name='password_reset'),
    url(r'^active/(?P<active_code>\w+)',ActiveUserView.as_view(),name='register'),
    url(r'^$',index,name='index'),
]