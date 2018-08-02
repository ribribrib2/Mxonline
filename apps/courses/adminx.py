import xadmin

from courses.models import Course,Lesson,Video,CourseResource

xadmin.site.register(Course)
xadmin.site.register(Lesson)
xadmin.site.register(Video)
xadmin.site.register(CourseResource)