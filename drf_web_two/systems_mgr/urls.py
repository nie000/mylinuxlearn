from django.urls import path
from django.views.decorators.cache import cache_page
from rest_framework import routers

from systems_mgr.views import EmployeeView, DepartmentView, \
    SalaryView, EmployeeUpdSalaryView, EmployeeAllView, EmployeeTitleInfo, DepSalaryView, EmpolyeeNameView, \
    PhoneCodeView, AreaProvince

# router = routers.SimpleRouter()
# router.register(r'api', ApiMgrView)

urlpatterns = [
    #作业
    path('employees/',EmployeeView.as_view({'post':'create','get':'list'})),
    path('departments/',DepartmentView.as_view({'post':'create','get':'list'})),
    path('salarys/',SalaryView.as_view({'post':'create'})),
    #5、
    path('employee/<int:pk>/',EmployeeUpdSalaryView.as_view({'put':'update'})),
    #6、
    path('department/<int:pk>/',DepartmentView.as_view({'post':'create','delete':'destroy'})),
    #9、
    path('employees_all/',EmployeeAllView.as_view({'get':'list'})),
    #11
    path('title_info/',cache_page(5)(EmployeeTitleInfo.as_view({'get':'list'}))),
    #12
    path('dep_salary/',cache_page(60 * 15)(DepSalaryView.as_view())),
    #13
    path('employee_name/',EmpolyeeNameView.as_view({'get':'list'})),
    #获取验证码
    path('phone_code/',PhoneCodeView.as_view({'post':'create'})),
    #省查询
    path('area_province/',AreaProvince.as_view({'get':'list'})),
]