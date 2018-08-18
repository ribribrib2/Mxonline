from django.shortcuts import render,get_object_or_404
from django.views.generic.base import View
from django.http import HttpResponse

from .models import CourseOrg,CityDict,Teacher
from .forms import UserAskForm
from courses.models import Course
from operation.models import UserFavorite

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.

class OrgView(View):
    def get(self,request):
        all_org = CourseOrg.objects.all()
        hot_org = CourseOrg.objects.all().order_by('-click_nums')[:3]
        all_city = CityDict.objects.all()
        city_id = request.GET.get('city', "")
        if city_id:
            all_org = all_org.filter(city_id=int(city_id))
        catrgory = request.GET.get('ct', "")
        if catrgory:
            all_org = all_org.filter(category=catrgory)
        sort = request.GET.get('sort', "")
        if sort:
            if sort == 'students':
                all_org = all_org.order_by('-students')
            if sort == 'courses':
                all_org = all_org.order_by('-couese_num')
        org_num = all_org.count()

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation
        p = Paginator(all_org,5, request=request)
        orgs = p.page(page)
        return render(request,'org-list.html',{
            'all_org':orgs,
            'all_city':all_city,
            'org_num':org_num,
            'city_id':city_id,
            'category':catrgory,
            'hot_org':hot_org,
            'sort':sort,
            'current_page':'organization',
        })


class AddUserAskView(View):
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True)
            # 如果保存成功,返回json字符串,后面content type是告诉浏览器返回的数据类型
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            # 如果保存失败，返回json字符串,并将form的报错信息通过msg传递到前端
            return HttpResponse('{"status":"fail", "msg":"添加出错"}', content_type='application/json')


class AddFavView(View):
    def post(self,request):
        id = request.POST.get('fav_id', 0)
        type = request.POST.get('fav_type', 0)
        if not request.user.is_authenticated:
            return HttpResponse("{'status':'fail','msg':'用户未登录'}",content_type='application/json')

        exist_record = UserFavorite.objects.filter(user=request.user,fav_id=int(id),fav_type=type)
        if exist_record:
            exist_record.delete()
            if int(type) == 1:
                course = Course.objects.get(id=int(id))
                course.fav_nums -= 1
                if course.fav_nums < 0:
                    course.fav_nums = 0
                course.save()
            elif int(type) == 2:
                org = CourseOrg.objects.get(id=int(id))
                org.fav_nums -= 1
                if org.fav_nums < 0:
                    org.fav_nums = 0
                org.save()
            elif int(type) == 3:
                teacher = Teacher.objects.get(id=int(id))
                teacher.fav_nums -= 1
                if teacher.fav_nums < 0:
                    teacher.fav_nums = 0
                teacher.save()
            return HttpResponse('{"status":"success", "msg":"收藏"}', content_type='application/json')
        else:
            user_fav = UserFavorite()
            if int(type) > 0 and int(id) > 0:
                user_fav.fav_id = int(id)
                user_fav.fav_type = int(type)
                user_fav.user = request.user
                user_fav.save()

                if int(type) == 1:
                    course = Course.objects.get(id=int(id))
                    course.fav_nums += 1
                    course.save()
                elif int(type) == 2:
                    org = CourseOrg.objects.get(id=int(id))
                    org.fav_nums += 1
                    org.save()
                elif int(type) == 3:
                    teacher = Teacher.objects.get(id=int(id))
                    teacher.fav_nums += 1
                    teacher.save()
                return HttpResponse('{"status":"success", "msg":"已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail", "msg":"收藏出错"}', content_type='application/json')


class OrgHomeView(View):
    def get(self,request,org_id):
        org = get_object_or_404(CourseOrg,id=org_id)
        courses = org.course_set.all()
        teachers = org.teacher_set.all()
        has_fav_org = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=org.id, fav_type=2):
                has_fav_org = True
        return render(request,'org-detail-homepage.html',{'org':org,
                                                          'courses':courses,
                                                          'teachers':teachers,
                                                          'current_page':'home',
                                                          'has_fav_org':has_fav_org})


class OrgCourseView(View):
    def get(self,request,org_id):
        org = get_object_or_404(CourseOrg,id=org_id)
        courses = org.course_set.all()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation
        p = Paginator(courses,5, request=request)
        courses = p.page(page)
        has_fav_org = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=org.id, fav_type=2):
                has_fav_org = True
        return render(request,'org-detail-course.html',{'org':org,
                                                          'courses':courses,
                                                          'current_page': 'course',
                                                        'has_fav_org':has_fav_org,})


class OrgDescView(View):
    def get(self,request,org_id):
        org = get_object_or_404(CourseOrg,id=org_id)
        has_fav_org = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=org.id, fav_type=2):
                has_fav_org = True
        return render(request,'org-detail-desc.html',{'org':org,
                                                          'current_page': 'desc',
                                                      'has_fav_org': has_fav_org})


class OrgTeacherView(View):
    def get(self,request,org_id):
        org = get_object_or_404(CourseOrg,id=org_id)
        teachers = org.teacher_set.all()
        has_fav_org = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=org.id, fav_type=2):
                has_fav_org = True
        return render(request,'org-detail-teachers.html',{'org':org,
                                                      'teachers':teachers,
                                                      'current_page': 'teacher',
                                                          'has_fav_org': has_fav_org})


class TeacherListView(View):
    def get(self,request):
        teachers = Teacher.objects.all()
        teacher_num = teachers.count()
        hot_teachers = teachers.order_by('click_nums')[:3]
        sort = request.GET.get('sort', "")
        if sort == 'hot':
            teachers = teachers.order_by('click_nums')
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation
        p = Paginator(teachers, 5, request=request)
        teachers = p.page(page)
        return render(request, 'teachers-list.html', {'teachers': teachers,
                                                      'teacher_num':teacher_num,
                                                      'hot_teachers':hot_teachers,
                                                      'sort':sort,
                                                      'current_page': 'teacher'})


class TeacherDetailView(View):
    def get(self,request,teacher_id):
        teacher = get_object_or_404(Teacher,id=teacher_id)
        courses = teacher.course_set.all()
        hot_teachers = Teacher.objects.all().order_by('click_nums')[:3]

        has_fav_teacher = False
        has_fav_org = False
        if UserFavorite.objects.filter(fav_id=teacher.id,fav_type=3):
            has_fav_teacher = True
        if UserFavorite.objects.filter(fav_id=teacher.org.id,fav_type=2):
            has_fav_org = True

        return render(request,'teacher-detail.html',{
            'teacher':teacher,
            'courses':courses,
            'hot_teachers':hot_teachers,
            'has_fav_teacher':has_fav_teacher,
            'has_fav_org':has_fav_org,
        })

