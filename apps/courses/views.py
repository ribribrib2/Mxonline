from django.shortcuts import render,get_object_or_404
from django.views.generic.base import View

from .models import Course

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
class CourseListView(View):
    def get(self,request):
        courses = Course.objects.all()
        hot_courses = courses.order_by('click_nums')[:3]
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation
        p = Paginator(courses,6, request=request)
        courses = p.page(page)
        return render(request,'course-list.html',{'courses':courses,
                                                  'current_page':'course',
                                                  'hot_courses':hot_courses})

class CourseDetailView(View):
    def get(self,request,course_id):
        course = get_object_or_404(Course,id=course_id)
        return render(request,'course-detail.html',{
            'course':course,
        })