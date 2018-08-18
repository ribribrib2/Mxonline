import xadmin

from courses.models import Course,Lesson,Video,CourseResource,BannerCourse,CourseCategory


class LessonInline(object):
    model = Lesson
    extra = 0


class CourseResourceInline(object):
    model = CourseResource
    extra = 0

class CourseCategoryAdmin(object):
    pass


class CourseAdmin(object):
    '''课程'''
    list_display = ['name', 'desc',  'degree', 'learn_times','get_learner_num']
    search_fields = ['name', 'desc', 'degree', 'get_learner_num']
    list_filter = ['name', 'desc', 'degree', 'learn_times', 'get_learner_num']
    model_icon = 'fa fa-book'            #图标
    inlines = [LessonInline, CourseResourceInline]  # 增加章节和课程资源

    # def queryset(self):
    #     # 重载queryset方法，来过滤出我们想要的数据的
    #     qs = super(CourseAdmin, self).queryset()
    #     # 只显示is_banner=True的课程
    #     qs = qs.filter(is_banner=False)
    #     return qs
    #
    # def save_models(self):
    #     # 在保存课程的时候统计课程机构的课程数
    #     # obj实际是一个course对象
    #     obj = self.new_obj
    #     # 如果这里不保存，新增课程，统计的课程数会少一个
    #     obj.save()
    #     # 确定课程的课程机构存在。
    #     if obj.course_org is not None:
    #         #找到添加的课程的课程机构
    #         course_org = obj.course_org
    #         #课程机构的课程数量等于添加课程后的数量
    #         course_org.course_nums = Course.objects.filter(course_org=course_org).count()
    #         course_org.save()


class BannerCourseAdmin(object):
    '''课程'''
    list_display = ['name', 'desc',  'degree', 'learn_times', 'get_learner_num']
    search_fields = ['name', 'desc', 'degree', 'get_learner_num']
    list_filter = ['name', 'desc', 'degree', 'learn_times', 'get_learner_num']
    model_icon = 'fa fa-book'            #图标
    inlines = [LessonInline, CourseResourceInline]  # 增加章节和课程资源

    # def queryset(self):
    #     # 重载queryset方法，来过滤出我们想要的数据的
    #     qs = super(BannerCourseAdmin, self).queryset()
    #     # 只显示is_banner=True的课程
    #     qs = qs.filter(is_banner=False)
    #     return qs


class LessonAdmin(object):
    '''章节'''

    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']
    # 这里course__name是根据课程名称过滤
    list_filter = ['course__name', 'name', 'add_time']


class VideoAdmin(object):
    '''视频'''

    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson', 'name', 'add_time']


class CourseResourceAdmin(object):
    '''课程资源'''

    list_display = ['course', 'name', 'download', 'add_time']
    search_fields = ['course', 'name', 'download']
    list_filter = ['course__name', 'name', 'download', 'add_time']


# 将管理器与model进行注册关联
xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(BannerCourse, CourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
xadmin.site.register(CourseCategory, CourseCategoryAdmin)