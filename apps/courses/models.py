from django.db import models
from organization.models import CourseOrg,Teacher

# Create your models here.
class Course(models.Model):
    '''课程'''
    DEGREE_CHOICES = (
        ("cj", "初级"),
        ("zj", "中级"),
        ("gj", "高级")
    )
    courseorg = models.ForeignKey(CourseOrg,verbose_name='所属机构',on_delete=models.CASCADE,default='')
    teacher = models.ForeignKey(Teacher,verbose_name='任课教师',on_delete=models.CASCADE,default='')
    name = models.CharField('课程名', max_length=50)
    desc = models.CharField('课程描述', max_length=300)
    detail = models.TextField('课程详情')
    degree = models.CharField('难度', choices=DEGREE_CHOICES, max_length=2)
    learn_times = models.IntegerField("学习时长(分钟数)", default=0)
    students = models.IntegerField("学习人数", default=0)
    fav_nums = models.IntegerField("收藏人数", default=0)
    image = models.ImageField("封面图", upload_to="courses/%Y/%m", max_length=100)
    click_nums = models.IntegerField("点击数", default=0)
    tag = models.CharField('课程标签', default='', max_length=10)
    is_banner = models.BooleanField('是否轮播', default=False)
    add_time = models.DateTimeField("添加时间", auto_now_add=True)

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Lesson(models.Model):
    '''课程章节'''
    course = models.ForeignKey(Course,verbose_name='课程',on_delete=models.CASCADE)
    name = models.CharField('章节名',max_length=100)
    add_time = models.DateTimeField('添加时间',auto_now_add=True)

    class Meta:
        verbose_name = '章节'
        verbose_name_plural = verbose_name


class Video(models.Model):
    '''章节视频'''
    lesson = models.ForeignKey(Lesson, verbose_name='章节',on_delete=models.CASCADE)
    name = models.CharField('视频名',max_length=100)
    url = models.CharField('访问地址',default='',max_length=200)
    learn_times = models.IntegerField('学习时长(分钟数)', default=0)
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


