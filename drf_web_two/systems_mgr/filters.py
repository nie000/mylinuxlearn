from django.db.models import QuerySet, Q
from django_filters import filters
from django_filters.rest_framework import FilterSet

from systems_mgr.models import Employee


class EmployeesFilter(FilterSet):
    ordering = filters.CharFilter(method='get_ordering',label='排序字段')  # 指定对应的方法
    name=filters.CharFilter(method='get_name',label='模糊查询用户名和职称')  # 指定对应的方法
    def get_ordering(self, queryset:QuerySet, name, value):
        # 多选项，由，号分割
        return queryset.order_by(value)
    def get_name(self, queryset:QuerySet, name, value):
        return queryset.filter(Q(name__contains=value)|Q(title__contains=value))
    class Meta:
        model=Employee
        fields = {
            'sex': ['iexact'],
            'birthday': ['gte', 'lte'],
        }
# Employee.objects.filter(Q(name__contains='')|Q(title__contains='')).order_by('-name')