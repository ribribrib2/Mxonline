from django.shortcuts import render
from django.contrib.auth import authenticate,login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from .models import UserProfile

class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None




# Create your views here.
def user_login(request):
    print(request.method)
    if request.method == 'POST':
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        print(username)
        print(password)
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return render(request,'index.html')
        else:
            return render(request,'login.html',{'msg':'用户名或密码错误'})
    elif request.method == 'GET':
        return render(request,'login.html')

def index(request):
    return render(request,'index.html')