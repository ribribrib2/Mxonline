import xadmin

from organization.models import CityDict,CourseOrg,Teacher

xadmin.site.register(CityDict)
xadmin.site.register(CourseOrg)
xadmin.site.register(Teacher)