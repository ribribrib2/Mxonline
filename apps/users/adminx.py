import xadmin

from users.models import UserProfile,EmailVerifyRecord,Banner

xadmin.site.unregister(UserProfile)
xadmin.site.register(UserProfile)
xadmin.site.register(EmailVerifyRecord)
xadmin.site.register(Banner)