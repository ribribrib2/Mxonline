# apps/utils/mixin_utils.py

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import reverse

# LOGIN_URL = reverse('users:login')
LOGIN_URL = '/users/login/'

class LoginRequiredMixin(object):
    @method_decorator(login_required(login_url=LOGIN_URL))
    def dispatch(self,request,*args,**kwargs):
        return super(LoginRequiredMixin, self).dispatch(request,*args,**kwargs)