from django.shortcuts import render,get_object_or_404
from django.views.generic.base import View
from django.http import HttpResponse

from .models import CourseOrg,CityDict,Teacher
from .forms import UserAskForms
from courses.models import Course

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
    def post(self,request):
        userask_form = UserAskForms(request.POST)
        if userask_form.is_valid():
            user_ask =userask_form.save(commit=True)
            return HttpResponse("{'status':'success'}",content_type='application/json')
        else:
            return HttpResponse("{'status':'fail','msg':'添加出错'}",content_type='application/json')


class OrgHomeView(View):
    def get(self,request,org_id):
        org = get_object_or_404(CourseOrg,id=org_id)
        courses = org.course_set.all()
        teachers = org.teacher_set.all()
        return render(request,'org-detail-homepage.html',{'org':org,
                                                          'courses':courses,
                                                          'teachers':teachers,
                                                          'current_page':'home'})

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
        return render(request,'org-detail-course.html',{'org':org,
                                                          'courses':courses,
                                                          'current_page': 'course'})

class OrgDescView(View):
    def get(self,request,org_id):
        org = get_object_or_404(CourseOrg,id=org_id)
        return render(request,'org-detail-desc.html',{'org':org,
                                                          'current_page': 'desc'})

class OrgTeacherView(View):
    def get(self,request,org_id):
        org = get_object_or_404(CourseOrg,id=org_id)
        teachers = org.teacher_set.all()
        return render(request,'org-detail-teachers.html',{'org':org,
                                                      'teachers':teachers,
                                                      'current_page': 'teacher'})

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
        return render(request,'teacher-detail.html',{
            'teacher':teacher,
            'courses':courses,
            'hot_teachers':hot_teachers
        })

