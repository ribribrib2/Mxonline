from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse

from .models import CourseOrg,CityDict,Teacher
from .forms import UserAskForms

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
        })

class AddUserAskView(View):
    def post(self,request):
        userask_form = UserAskForms(request.POST)
        if userask_form.is_valid():
            user_ask =userask_form.save(commit=True)
            return HttpResponse("{'status':'success'}",content_type='application/json')
        else:
            return HttpResponse("{'status':'fail','msg':'添加出错'}",content_type='application/json')


