from django import forms
from captcha.fields import CaptchaField
from .models import UserProfile

class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True,min_length=8)


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True,min_length=8)
    captcha = CaptchaField(error_messages={'invalid':'验证码错误'})

class ForgetForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={'invalid':'验证码错误'})

class PasswordModifyForm(forms.Form):
    password_new1 = forms.CharField(required=True, min_length=8)
    password_new2 = forms.CharField(required=True, min_length=8)

class PasswordResetForm(forms.Form):
    password_old = forms.CharField(required=True, min_length=8)
    password_new1 = forms.CharField(required=True, min_length=8)
    password_new2 = forms.CharField(required=True, min_length=8)

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']

class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nick_name','birday','genber','address','mobile']