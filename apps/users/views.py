from django.shortcuts import render,HttpResponse,redirect,reverse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.views.generic.base import View
from utils.email_send import SendEmail

from .models import UserProfile,EmailVerifyRecord
from .forms import LoginForm,RegisterForm,ForgetForm,PasswordResetForm


#邮箱和用户名都可以登录
#基与ModelBackend类，因为它有authenticate方法
class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            #不希望用户存在两个，get只能有一个。两个是get失败的一种原因 Q为使用并集查询
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            # django的后台中密码加密：所以不能password==password
            # UserProfile继承的AbstractUser中有def check_password(self, raw_password):
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class IndexView(View):
    def get(self,request):
        return render(request, 'email_send.html')


#登录
class LoginView(View):
    '''用户登录'''

    def get(self,request):
        return render(request, 'login.html')

    def post(self,request):
        #实例化
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            #获取用户提交的用户名和密码
            username = request.POST.get('username','')
            password = request.POST.get('password','')
            #成功返回user对象,失败None
            user = authenticate(username=username,password=password)
            if user is not None:
                #只有注册激活才能登录
                if user.is_active:
                    login(request,user)
                    return redirect(reverse('index'))
                else:
                    return render(request, 'login.html', {'login_form':login_form,'msg': '用户未激活'})
            else:
                return render(request, 'login.html', {'login_form':login_form,'msg': '用户名或密码错误'})
        else:
            return render(request,'login.html',{'login_form':login_form})


class LogoutView(View):
    def get(self,request):
        logout(request)
        return redirect(reverse('users:login'))


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
            return render(request, 'email_send.html')
        else:
            return render(request,'register.html',{'register_form':register_form})


class ActiveUserView(View):
    def get(self,request,active_code):
        record = EmailVerifyRecord.objects.get(code=active_code)
        if record and record.is_active == True:
            record.is_active = False
            record.save()
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
        if passwordResetCode and passwordResetCode.is_active == True:
            passwordResetCode.is_active = False
            passwordResetCode.save()
            passwordreset_form = PasswordResetForm()
            email = passwordResetCode.email
            return render(request, 'password_reset.html',{'passwordreset_form':passwordreset_form,'email':email,'password_modify_status':False})
        else:
            return HttpResponse('该链接无效')


class ModifyPwdView(View):
    def post(self,request):
        passwordreset_form = PasswordResetForm(request.POST)
        email = request.POST.get('email', None)
        if passwordreset_form.is_valid():
            password = request.POST.get('password', None)
            password2 = request.POST.get('password2', None)
            if password != password2:
                render(request,'password_reset.html',{'error_message':'两次输入密码不一样'})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(password)
            user.save()
            return render(request,'password_reset.html',{'password_modify_status':True})
        else:
            return render(request, 'password_reset.html', {'passwordreset_form': passwordreset_form,'email':email,'password_modify_status':False})
