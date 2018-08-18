from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class UserProfile(AbstractUser):
    nick_name = models.CharField('昵称',max_length=20)
    birday = models.DateField('生日',null=True,blank=True)
    genber = models.CharField('性别',choices=(('male','男'),('female','女')),default='male',max_length=10)
    address = models.CharField('地址',max_length=50,null=True,blank=True)
    mobile = models.CharField('联系方式',max_length=11,null=True,blank=True)
    image = models.ImageField('头像',upload_to='user_image/%Y/%m/',default='user_image/default.png')

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

class EmailVerifyRecord(models.Model):
    code = models.CharField('验证码',max_length=20)
    email = models.EmailField('邮箱')
    send_type = models.CharField('类型',choices=(('register','注册'),('forget','找回密码')),max_length=20)
    send_time = models.DateTimeField('发送时间',auto_now_add=True)
    is_active = models.BooleanField('是否有效',default=False)

    class Meta:
        verbose_name = '验证码'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{}({})'.format(self.code,self.email)

class Banner(models.Model):
    title = models.CharField('标题',max_length=100)
    image = models.ImageField('轮播图',upload_to='banner/%Y/%m',max_length=100,blank=True)
    url = models.URLField('访问地址')
    index = models.IntegerField('顺序',default=100)
    add_time = models.DateTimeField('添加时间',auto_now_add=True)

    class Meta:
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name