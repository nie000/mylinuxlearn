import random

from django.core.cache import cache
from django.db.models import Count, Sum, Max
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.models import User
# Create your views here.
from django.views import View
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, serializers
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, \
    DestroyModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSetMixin, GenericViewSet, ModelViewSet, ReadOnlyModelViewSet

# from common_fun.my_apiview import APIView, APIQuerysetMinx, APIListMixin, APISingleObjectMixin, APIDetailMixin, \
#     APICreateMixin, APIUpdateMixin, APIMethodMapMixin


# class UserList(APIView,APIQuerysetMinx):
#     model = User
#     def get(self,request,*args,**kwargs):
#         return self.response(queryset=self.get_queryset(),fields=('last_name','username'))
from rest_framework_simplejwt import authentication
from rest_framework_simplejwt.views import TokenViewBase

from common_fun.code import send_msg
from common_fun.my_pagination import TwoPagePagination
from common_fun.my_permissions import MyPermiss, NomalPermiss, RootPermiss

from systems_mgr.filters import EmployeesFilter
from systems_mgr.models import ApiMgr, Grade, Employee, Department, Salary, AreaCity
from systems_mgr.serializers import UserSerializers, ApiMgrSerializers, GradeSerializer, EmployeeSerializer, \
    DepartmentSerializer, SalarySerializer, EmployeeUpdSalarySerializer, EmployeeAllSerializer, \
    EmployeeTitleInfoSerializer, DepSalarySerializer, EmpolyeeNameSerializer, PhoneTokenRefreshSerializer, \
    PhoneUserNameSerializer, AreaProvinceSerializer


class EmployeeView(GenericViewSet,CreateModelMixin,ListModelMixin):
    serializer_class =EmployeeSerializer
    queryset = Employee.objects.all()
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['name', 'sex']
    # filter_backends = [SearchFilter]
    # search_fields = ['name','title']
    # filter_backends = [OrderingFilter]
    # ordering_fields = ['name', 'title']
    # filter_backends = [DjangoFilterBackend]
    # filter_class =EmployeesFilter
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['name', 'title']
    ordering_fields = ['name', 'title']
    permission_classes = [RootPermiss]

#包含第10题
class DepartmentView(GenericViewSet,CreateModelMixin,DestroyModelMixin,ListModelMixin):
    serializer_class =DepartmentSerializer
    queryset = Department.objects.all()

class SalaryView(GenericViewSet,CreateModelMixin):
    serializer_class =SalarySerializer
    queryset = Salary.objects.all()

#5
class EmployeeUpdSalaryView(GenericViewSet,UpdateModelMixin):
    serializer_class = EmployeeUpdSalarySerializer
    queryset = Employee.objects.all()
#9
class EmployeeAllView(GenericViewSet,ListModelMixin):
    serializer_class = EmployeeAllSerializer
    queryset = Employee.objects.all()

#11
class EmployeeTitleInfo(GenericViewSet,ListModelMixin):
    serializer_class = EmployeeTitleInfoSerializer
    queryset = Employee.objects.all()
    def get_queryset(self):
        return self.queryset.values('title').annotate(title_num=Count('empid'))

#12
class DepSalaryView(GenericAPIView,ListModelMixin):
    serializer_class=DepSalarySerializer
    queryset = Employee.objects.all()
    pagination_class = TwoPagePagination
    def get_queryset(self):
        return self.queryset.values('department__depname').annotate(
    salary_sum=Sum('salary__basesalary')+Sum('salary__titlesalary')-Sum('salary__deduction'),
    salary_avg=(Sum('salary__basesalary')+Sum('salary__titlesalary')-Sum('salary__deduction'))/Count('empid'))
    # @cache_page(60 * 15)
    @swagger_auto_schema(operation_summary='分组统计部门工资', operation_id='部门工资统计')
    def get(self,request,*args,**kwargs):
        """
        根据部门的名称，分组统计所有部门员工的工资总数和平均工资
        """
        return self.list(request,*args,**kwargs)

#13
class EmpolyeeNameView(GenericViewSet,ListModelMixin):
    serializer_class=EmpolyeeNameSerializer
    queryset = Employee.objects.all()
    # permission_classes = (permissions.IsAuthenticated,)
    pagination_class = TwoPagePagination
    def get_queryset(self):
        max_salary = self.queryset.filter(department__depname='销售部').aggregate(Max('salary__basesalary'))
        return self.queryset.filter(salary__basesalary__gt=max_salary['salary__basesalary__max']).values('name')

class PhoneTokenObtainPairView(TokenViewBase):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    """
    serializer_class = PhoneTokenRefreshSerializer


# 前端获取用户名
# 后端通过用户名查询手机号
# 生成验证码并存储到本地
# 然后发送短信给手机号(包含验证码)

class PhoneCodeView(GenericViewSet,CreateModelMixin):
    serializer_class =PhoneUserNameSerializer
    def perform_create(self, serializer:Serializer):
        phone=serializer.validated_data['username']
        num_code = random.randint(100000, 999999)
        # result=send_msg(phone,num_code)
        cache.set(phone,num_code,60)
        print(num_code)
        # if result==False:
        #     raise serializers.ValidationError('验证码发送失败！',code='send_error')

class AreaProvince(GenericViewSet,ListModelMixin):
    serializer_class =AreaProvinceSerializer
    queryset = AreaCity.objects.all().order_by('-area_sort')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['area_parent__id','area_type']