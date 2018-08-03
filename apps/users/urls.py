from django.conf.urls import url

from .views import user_login,index

urlpatterns = [
    url(r'^login/$',user_login,name='login'),
    url(r'^$',index,name='index'),
]