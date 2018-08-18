from django.db import models
from django.db.models import Sum
from organization.models import CourseOrg,Teacher

class CourseCategory(models.Model):
    name = models.CharField('分类',max_length=20)

    class Meta:
        verbose_name = '课程分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

# Create your models here.
class Course(models.Model):
    '''课程'''
    DEGREE_CHOICES = (
        ("cj", "初级"),
        ("zj", "中级"),
        ("gj", "高级")
    )
    courseorg = models.ForeignKey(CourseOrg,verbose_name='课程机构',on_delete=models.CASCADE,blank=True,null=True)
    teacher = models.ForeignKey(Teacher,verbose_name='任课教师',on_delete=models.CASCADE)
    name = models.CharField('课程名', max_length=50)
    desc = models.TextField('课程描述')
    detail = models.TextField('课程详情')
    degree = models.CharField('难度', choices=DEGREE_CHOICES, max_length=2)
    fav_nums = models.IntegerField("收藏人数", default=0)
    image = models.ImageField("封面图", upload_to="courses/%Y/%m", max_length=100,blank=True)
    click_nums = models.IntegerField("点击数", default=0)
    categorys = models.ForeignKey(CourseCategory,verbose_name='课程类别',on_delete=models.CASCADE)
    youneed_know = models.TextField('课程须知')
    teacher_tell = models.TextField('老师告诉你')
    add_time = models.DateTimeField("添加时间", auto_now_add=True)
    is_banner = models.BooleanField('是否轮播', default=False)
    announcement = models.TextField('课程公告',default='')

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_zj_nums(self):
        #获取课程章节数
        return self.lesson_set.count()
    get_zj_nums.short_description = '章节数'

    def get_learn_time(self):
        #获取所有课程的累积时间
        learn_time = 0
        all_lesson = self.lesson_set.all()
        for lesson in all_lesson:
            Lesson = lesson.video_set.aggregate(times=Sum('learn_times'))
            learn_time += Lesson['times']
        return learn_time
    get_learn_time.short_description = '学习时长'

    def get_course_lesson(self):
        #获取课程所有章节
        return self.lesson_set.all()

    def get_learn_user(self):
        #获取学习这门课的5位用户
        return self.usercourse_set.all()[:5]

    def get_learner_num(self):
        #获取该课程学习人数
        return self.usercourse_set.count()
    get_learner_num.short_description = '学习人数'

class BannerCourse(Course):
    class Meta:
        verbose_name = '轮播课程'
        verbose_name_plural = verbose_name
        # 这里必须设置proxy=True，这样就不会在生成一张表，而且具有Model的功能
        proxy = True


class Lesson(models.Model):
    '''课程章节'''
    course = models.ForeignKey(Course,verbose_name='课程',on_delete=models.CASCADE)
    name = models.CharField('章节名',max_length=100)
    add_time = models.DateTimeField('添加时间',auto_now_add=True)

    class Meta:
        verbose_name = '章节'
        verbose_name_plural = verbose_name

    def get_lesson_vedio(self):
        # 获取章节所有视频
        return self.video_set.all()

    def __str__(self):
        return '《{0}》课程的章节 >> {1}'.format(self.course,self.name)


class Video(models.Model):
    '''章节视频'''
    lesson = models.ForeignKey(Lesson, verbose_name='章节',on_delete=models.CASCADE)
    name = models.CharField('视频名',max_length=100)
    url = models.CharField('访问地址',default='',max_length=200)
    learn_times = models.PositiveSmallIntegerField('学习时长(分钟数)', default=0)
    add_time = models.DateTimeField('添加时间',auto_now_add=True)

    class Meta:
        verbose_name = "视频"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name='课程',on_delete=models.CASCADE)
    name = models.CharField('名称',max_length=100)
    download = models.FileField('资源文件',upload_to="course/resource/%Y/%m",max_length=100)
    add_time = models.DateTimeField('添加时间', auto_now_add=True)

    class Meta:
        verbose_name = "课程资源"
        verbose_name_plural = verbose_name


