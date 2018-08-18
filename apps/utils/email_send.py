import random

from django.core.mail import send_mail

from users.models import EmailVerifyRecord
from Mxonline.setting_dev import DEFAULT_FROM_EMAIL


def random_str(random_length=8):
    str = ''
    Chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz01234567890'
    lens = len(Chars) - 1
    for i in range(random_length):
        str += Chars[random.randint(0,lens)]
    return str


def SendEmail(email,send_type = 'register'):
    email_verifyrecied = EmailVerifyRecord()
    email_verifyrecied.code = random_str(16)
    email_verifyrecied.email = email
    email_verifyrecied.send_type = send_type
    email_verifyrecied.is_active = True
    email_verifyrecied.save()

    if send_type == 'register':
        Email_title = 'Mxonline账号注册激活链接'
        Email_body = '请点击下发链接激活账号:http://127.0.0.1:8000/email-verify/{0}'.format(email_verifyrecied.code)

        return send_mail(Email_title,Email_body,DEFAULT_FROM_EMAIL,[email])


    if send_type == 'forget':
        Email_title = 'Mxonline账号找回密码链接'
        Email_body = '请点击下发链接激活账号:http://127.0.0.1:8000/email-verify/{0}'.format(email_verifyrecied.code)

        return send_mail(Email_title, Email_body, DEFAULT_FROM_EMAIL, [email])



