from django.conf.urls import url
from django.contrib.sessions.middleware import SessionMiddleware
from .views import index,LoginView

urlpatterns = [
    url(r'^login/$',LoginView.as_view(),name='login'),
    url(r'^$',index,name='index'),
]