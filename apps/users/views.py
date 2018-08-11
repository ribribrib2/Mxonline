import json

from django.shortcuts import render,HttpResponse,redirect,reverse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.views.generic.base import View
from utils.email_send import SendEmail
from utils.mixin_utils import LoginRequiredMixin

from .models import UserProfile,EmailVerifyRecord
from .forms import LoginForm,RegisterForm,ForgetForm,PasswordModifyForm,PasswordResetForm,ImageUploadForm,UserInfoForm


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

#主页
class IndexView(View):
    def get(self,request):
        return render(request, 'index.html',{
            'current_page':'index'
        })


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


#登出
class LogoutView(LoginRequiredMixin,View):
    '''用户登出'''

    def get(self,request):
        logout(request)
        return redirect(reverse('users:login'))


#注册
class RegisterView(View):
    '''用户注册'''

    def get(self,request):
        register_form = RegisterForm()
        return render(request,'register.html',{'register_form':register_form})

    def post(self,request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_email = request.POST.get('email',None)
            #如果该账号已经注册,报错
            if UserProfile.objects.filter(email=user_email):
                return render(request, 'register.html',{'register_form':register_form,'error_message':'该账号已经注册'})
            user_password = request.POST.get('password', None)
            user_profile = UserProfile()
            user_profile.username = user_email
            user_profile.email = user_email
            user_profile.password = make_password(user_password)
            user_profile.is_active = False
            user_profile.save()
            SendEmail(user_email,'register')
            return render(request, 'email-send.html', {'email':user_email})
        else:
            return render(request,'register.html',{'register_form':register_form})


#忘记密码
class PasswordForgetView(View):
    '''忘记密码'''

    def get(self,request):
        forget_form = ForgetForm()
        return render(request,'forgetpwd.html',{'forget_form':forget_form})

    def post(self,request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            user_email = request.POST.get('email',None)
            #Query不为空返回Ture
            if UserProfile.objects.filter(email=user_email).exists():
                SendEmail(user_email, 'forget')
                return render(request,'email-send.html',{'email':user_email})
            return render(request, 'forgetpwd.html', {'forget_form': forget_form,'error_message':'该账号未注册'})
        else:
            return render(request, 'forgetpwd.html',{'forget_form':forget_form})


# 重置密码
class PasswordResetView(LoginRequiredMixin,View):
    '''重置密码'''

    # def get(self,request):
    #     passwordreset_form = PasswordResetForm()
    #     return render(request,'password_reset.html',{'passwordreset_form':passwordreset_form})

    def post(self,request):
        passwordreset_form = PasswordResetForm(request.POST)
        if passwordreset_form.is_valid():
            password_old = request.POST.get('password_old','')
            password_new1 = request.POST.get('password_new1','')
            password_new2 = request.POST.get('password_new2','')
            user_email = request.POST.get('email','')
            user = UserProfile.objects.get(email=user_email)
            if make_password(password_old) != make_password(user.password):
                return render(request, 'password_reset.html',{'passwordreset_form': passwordreset_form, 'meg': '旧密码错误'})
            elif password_new1 != password_new2:
                return render(request,'password_reset.html',{'passwordreset_form':passwordreset_form,'meg':'两次密码不一样'})
            else:
                user.password = make_password(password_new1)
                user.save()
                return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(passwordreset_form.errors), content_type='application/json')


#邮箱链接验证
class EmailVerifyView(View):
    def get(self,request,verify_record):
        try:
            record =  EmailVerifyRecord.objects.get(code=verify_record)
        except Exception as e:
            record = None
        if record:
            if record.send_type == 'forget':
                if record.is_active == True:
                    record.is_active = False
                    record.save()
                    passwordmodify_form = PasswordModifyForm()
                    email = record.email
                    return render(request, 'password-modify.html',{'passwordmodify_form':passwordmodify_form,'email':email,'password_modify_status':False})
                else:
                    return HttpResponse('该链接无效')
            elif record.send_type == 'register':
                if record.is_active == True:
                    record.is_active = False
                    record.save()
                    email = record.email
                    user = UserProfile.objects.get(email=email)
                    user.is_active = True
                    user.save()
                    return render(request, 'email-verify.html', {'verify_status': True})
                else:
                    return render(request, 'email-verify.html', {'verify_status': False})
        else:
            return HttpResponse('该链接无效')


#修改密码
class ModifyPwdView(LoginRequiredMixin,View):
    def post(self,request):
        passwordmodify_form = PasswordModifyForm(request.POST)
        email = request.POST.get('email', None)
        if passwordmodify_form.is_valid():
            password_new1 = request.POST.get('password_new1', None)
            password_new2 = request.POST.get('password_new2', None)
            if password_new1 != password_new2:
                render(request,'password_reset.html',{'error_message':'两次输入密码不一样'})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(password_new1)
            user.save()
            return render(request,'password_reset.html',{'password_modify_status':True})
        else:
            return render(request, 'password_reset.html', {'passwordmodify_form': passwordmodify_form,'email':email,'password_modify_status':False})


#用户信息
class UserInfoView(LoginRequiredMixin,View):
    def get(self,request):
        return render(request,'usercenter-info.html')

    # url(r'^mycourse',UserInfoView.as_view(),name='mycourse'),
    # url(r'^fav-course',UserInfoView.as_view(),name='fav_course'),
    # url(r'^message',UserInfoView.as_view(),name='message'),

class ImageUploadView(LoginRequiredMixin,View):
    def post(self,request):
        imageupload_form = ImageUploadForm(request.POST,request.FILES)
        if imageupload_form.is_valid():
            image = imageupload_form.cleaned_data['image']
            request.user.image = image
            request.user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')

# class PasswordUploadView(View):

