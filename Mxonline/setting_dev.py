# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'Mxonline',
        'USER': 'root',
        'PASSWORD': '1235875995rib.',
        'HOST':'47.97.122.241',
        'POST':'3306',
    }
}

# 邮箱配置
EMAIL_HOST = 'smtp.163.com'
EMAIL_HOST_USER = '15384027261@163.com'
EMAIL_HOST_PASSWORD = '1235875995rib'  # 这个不是邮箱密码，而是授权码
EMAIL_PORT = 465  # 由于阿里云的25端口打不开，所以必须使用SSL然后改用465端口
# 是否使用了SSL 或者TLS，为了用465端口，要使用这个
EMAIL_USE_SSL = True
# 默认发件人，不设置的话django默认使用的webmaster@localhost，所以要设置成自己可用的邮箱
DEFAULT_FROM_EMAIL = 'Mxonline <15384027261@163.com>'