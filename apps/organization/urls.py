from django.conf.urls import url

from .views import OrgView,AddUserAskView
# from .views import PasswordUploadView

urlpatterns = [
    url(r'^org_list/$',OrgView.as_view(),name='org_list'),
    url(r'^add_ask/$',AddUserAskView.as_view(),name='add_ask'),
]
