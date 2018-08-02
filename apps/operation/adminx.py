import xadmin

from operation.models import UserAsk,CourseComments,UserFavorite,UserMessage,UserCourse

xadmin.site.register(UserAsk)
xadmin.site.register(CourseComments)
xadmin.site.register(UserFavorite)
xadmin.site.register(UserMessage)
xadmin.site.register(UserCourse)