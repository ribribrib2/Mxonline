from django.shortcuts import render,get_object_or_404,HttpResponse
from django.views.generic.base import View

from .models import Course,CourseResource,Video
from operation.models import UserCourse,UserFavorite,CourseComments
from utils.mixin_utils import LoginRequiredMixin

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
class CourseListView(View):
    #课程列表
    def get(self,request):
        all_courses = Course.objects.all().order_by('-add_time')
        #热门课程推荐
        hot_courses = all_courses.order_by('click_nums')[:3]
        sort = request.GET.get('sort','')
        #排序
        if sort:
            if sort == 'students':
                all_courses = all_courses.order_by('-students')
            if sort == 'hot':
                all_courses = all_courses.order_by('-click_nums')
        #分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation
        p = Paginator(all_courses,6, request=request)
        all_courses = p.page(page)
        return render(request,'course-list.html',{
            'all_courses':all_courses,
            'current_page':'course',
            'hot_courses':hot_courses,
            'sort':sort
        })

class CourseDetailView(View):
    def get(self,request,course_id):
        course = get_object_or_404(Course,id=course_id)
        #课程点击数加1
        course.click_nums += 1
        course.save()
        #收藏
        has_fav_course = False
        has_fav_org = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user,fav_id=course.id,fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user,fav_id=course.courseorg.id,fav_type=2):
                has_fav_org = True
        #相关课程推荐
        if course.categorys:
            relate_courses = Course.objects.filter(categorys=course.categorys).exclude(id=course.id)[:3]
        else:
            relate_courses = []
        return render(request,'course-detail.html',{
            'course':course,
            'relate_courses':relate_courses,
            'has_fav_course': has_fav_course,
            'has_fav_org': has_fav_org,
        })

class CourseInfoView(LoginRequiredMixin,View):
    #课程详情
    def get(self,request,course_id):
        user = request.user
        course = get_object_or_404(Course,id=course_id)
        #如果该学员没有在学该课程,添加
        if not UserCourse.objects.filter(user=user,course=course):
            UserCourse.objects.create(user=user,course=course)
        #学过该课程的学员
        users = course.usercourse_set.all()
        #列出学员ID
        users_id = [user.user.id for user in users]
        #找出这部分学员学过的所有课程
        all_user_courses = UserCourse.objects.filter(user_id__in=users_id)
        #找出这部分课程的ID
        courses_id = [user_course.course.id for user_course in all_user_courses]
        #找出这部分课程
        relate_courses = Course.objects.filter(id__in=courses_id).exclude(id=course.id).order_by('-click_nums')[:3]

        #课程资源
        resources = CourseResource.objects.filter(course=course)
        return render(request,'course-video.html',{
            'course':course,
            'resources':resources,
            'relate_courses':relate_courses,
        })


class CourseCommentsView(LoginRequiredMixin,View):
    #课程评论
    def get(self,request,course_id):
        course = get_object_or_404(Course,id=course_id)
        all_comments = CourseComments.objects.filter(course=course).order_by('-add_time')
        #学过该课程的学员
        users = course.usercourse_set.all()
        #列出学员ID
        users_id = [user.user.id for user in users]
        #找出这部分学员学过的所有课程
        all_user_courses = UserCourse.objects.filter(user_id__in=users_id)
        #找出这部分课程的ID
        courses_id = [user_course.course.id for user_course in all_user_courses]
        #找出这部分课程
        relate_courses = Course.objects.filter(id__in=courses_id).exclude(id=course.id).order_by('-click_nums')[:3]

        return render(request,'course-comment.html',{
            'course':course,
            'all_comments':all_comments,
            'relate_courses':relate_courses,
        })


class CourseAddCommentsView(View):
    #添加评论
    def post(self,request):
        course_id = request.POST.get('course_id','')
        comments = request.POST.get('comments','')
        course = get_object_or_404(Course,id=course_id)
        if not request.user.is_authenticated:
            return HttpResponse('{"status":"fail","msg":"用户未登录"}', content_type='application/json')
        CourseComments.objects.create(user=request.user,course=course,comments=comments)
        return HttpResponse('{"status":"success","msg":"评论成功"}', content_type='application/json') #' "" "" '


class CourseVideoPlayView(View):
    def get(self,request,video_id):
        video = get_object_or_404(Video,id=video_id)
        course = video.lesson.course
        user = request.user
        #如果该学员没有在学该课程,添加
        if not UserCourse.objects.filter(user=user,course=course):
            UserCourse.objects.create(user=user,course=course)
        #学过该课程的学员
        users = course.usercourse_set.all()
        #列出学员ID
        users_id = [user.user.id for user in users]
        #找出这部分学员学过的所有课程
        all_user_courses = UserCourse.objects.filter(user_id__in=users_id)
        #找出这部分课程的ID
        courses_id = [user_course.course.id for user_course in all_user_courses]
        #找出这部分课程
        relate_courses = Course.objects.filter(id__in=courses_id).exclude(id=course.id).order_by('-click_nums')[:3]

        #课程资源
        resources = CourseResource.objects.filter(course=course)
        return render(request,'course-play.html',{
            'course':course,
            'resources':resources,
            'relate_courses':relate_courses,
            'video':video,
        })