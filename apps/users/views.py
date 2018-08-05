from django.shortcuts import render,HttpResponse
from django.contrib.auth import authenticate,login
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.views.generic.base import View
from utils.email_send import SendEmail

from .models import UserProfile,EmailVerifyRecord
from .forms import LoginForm,RegisterForm,ForgetForm,PasswordResetForm


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


def index(request):
    return render(request,'index.html')


class LoginView(View):
    def get(self,request):
        return render(request, 'login.html')
    def post(self,request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST.get('username','')
            password = request.POST.get('password','')
            user = authenticate(username=username,password=password)
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return render(request,'index.html')
                else:
                    return render(request, 'login.html', {'msg': '用户未激活'})
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误'})
        else:
            return render(request,'login.html',{'login_form':login_form})


class RegisterView(View):
    def get(self,request):
        register_form = RegisterForm()
        return render(request,'register.html',{'register_form':register_form})
    def post(self,request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_email = request.POST.get('email',None)
            user_password = request.POST.get('password',None)
            if UserProfile.objects.filter(email=user_email):
                return render(request, 'register.html',{'register_form':register_form,'error_message':'该账号已经注册'})
            user_profile = UserProfile()
            user_profile.username = user_email
            user_profile.email = user_email
            user_profile.password = make_password(user_password)
            user_profile.is_active = False
            user_profile.save()
            SendEmail(user_email,'register')
            return render(request, 'login.html')
        else:
            return render(request,'register.html',{'register_form':register_form})


class ActiveUserView(View):
    def get(self,request,active_code):
        record = EmailVerifyRecord.objects.get(code=active_code)
        if record:
            email = record.email
            user = UserProfile.objects.get(email=email)
            user.is_active = True
            user.save()
        return render(request,'login.html')


class ForgetView(View):
    def get(self,request):
        forget_form = ForgetForm()
        return render(request,'forgetpwd.html',{'forget_form':forget_form})
    def post(self,request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            user_email = request.POST.get('email',None)
            if UserProfile.objects.filter(email=user_email) is None:
                return render(request, 'forgetpwd.html', {'forget_form': forget_form,'error_message':'该账号未注册'})
            SendEmail(user_email, 'forget')
            return HttpResponse('邮件已经发送')
        else:
            return render(request, 'forgetpwd.html',{'forget_form':forget_form})


class PasswordResetView(View):
    def get(self,request,passwordreset_code):
        passwordResetCode =  EmailVerifyRecord.objects.get(code=passwordreset_code)
        if passwordResetCode:
            passwordreset_form = PasswordResetForm()
            email = passwordResetCode.email
            return render(request, 'password_reset.html',{'passwordreset_form':passwordreset_form,'email':email})
        else:
            return HttpResponse('该链接无效')
    def post(self,request):
        passwordreset_form = PasswordResetForm(request.POST)
        if passwordreset_form.is_valid():
            password = request.POST.get('password', None)
            password2 = request.POST.get('password2', None)
            email = request.POST.get('email', None)
            if password != password2:
                render(request,'password_reset.html',{'error_message':'两次输入密码不一样'})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(password)
            user.save()
            return render(request,'login.html')
        else:
            return render(request, 'password_reset.html', {'passwordreset_form': passwordreset_form})

