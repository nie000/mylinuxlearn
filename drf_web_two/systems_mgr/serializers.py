from django.contrib.auth.models import User
from django.core.cache import cache
from django.db import transaction
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import Serializer, ModelSerializer, HyperlinkedModelSerializer, \
    raise_errors_on_nested_writes
from rest_framework.utils import model_meta
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from systems_mgr.models import ApiMgr, Student, Grade, Employee, Department, Salary, Users, AreaCity


class UserSerializers(ModelSerializer):
    class Meta:
        model=User
        fields='__all__'

class ApiMgrSerializers(ModelSerializer):
    # test_name=serializers.CharField(label='标题',help_text='测试描述',max_length=20,initial='/logout/')
    class Meta:
        model=ApiMgr
        fields='__all__'
        extra_kwargs={
            'api_name':{'help_text':'接口名称'}
        }

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Student
        fields='__all__'


class GradeSerializer(serializers.ModelSerializer):
    # student_set = serializers.SlugRelatedField(many=True,slug_field='age',read_only=True)
    student_set=StudentSerializer(many=True,read_only=True)
    class Meta:
        model = Grade
        fields = ['name', 'max_student', 'student_set']

#作业
#前四题  ，包含7题
class EmployeeSerializer(serializers.ModelSerializer):
    real_salary=SerializerMethodField()
    should_salary=SerializerMethodField()
    class Meta:
        model=Employee
        fields='__all__'
        extra_kwargs = {
            'sex': {'help_text': '1是男，0是女','write_only':True},
            'title':{'write_only':True},
            'birthday':{'write_only':True},
            'department': {'write_only': True},
            'salary': {'write_only': True}
        }
    def get_real_salary(self,obj):
        return obj.salary.basesalary + obj.salary.titlesalary - obj.salary.deduction
    def get_should_salary(self,obj):
        return obj.salary.basesalary+obj.salary.titlesalary
    def validate_birthday(self, value):
        if str(value)<'1980-01-01':
            raise serializers.ValidationError('必须是80后！')
        return value
#包含第10题
class EmployeeNameSalaryInfo(serializers.ModelSerializer):
    basesalary = serializers.IntegerField(source='salary.basesalary', label='基本工资')
    class Meta:
        model=Employee
        fields=['name','basesalary']


class DepartmentSerializer(serializers.ModelSerializer):
    employee_set=EmployeeNameSalaryInfo(many=True,read_only=True)
    class Meta:
        model=Department
        fields='__all__'
        # extra_kwargs = {
        #     'descripations': {'write_only': True}
        # }

class SalarySerializer(serializers.ModelSerializer):
    class Meta:
        model=Salary
        fields='__all__'
#第五题
class EmployeeUpdSalarySerializer(serializers.ModelSerializer):
    basesalary=serializers.IntegerField(label='基本工资')
    titlesalary=serializers.IntegerField(label='职务工资')
    class Meta:
        model=Employee
        fields=['title','basesalary','titlesalary']
    def update(self, instance:Employee, validated_data):
        raise_errors_on_nested_writes('update', self, validated_data)
        info = model_meta.get_field_info(instance)

        # Simply set each attribute on the instance, and then save it.
        # Note that unlike `.create()` we don't need to treat many-to-many
        # relationships as being a special case. During updates we already
        # have an instance pk for the relationships to be associated with.
        m2m_fields = []
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                m2m_fields.append((attr, value))
            else:
                setattr(instance, attr, value)
                # instance.title='工程师'
                # setattr(instance,'title','工程师')
        with transaction.atomic():
            instance.save()
            instance.salary.basesalary=validated_data.get('basesalary')
            instance.salary.titlesalary = validated_data.get('titlesalary')
            instance.salary.save()
        # Note that many-to-many fields are set after updating instance.
        # Setting m2m fields triggers signals which could potentially change
        # updated instance and we do not want it to collide with .update()
        for attr, value in m2m_fields:
            field = getattr(instance, attr)
            field.set(value)

        return instance

class EmployeeAllSerializer(serializers.ModelSerializer):
    real_salary = SerializerMethodField()
    depname=serializers.CharField(source='department.depname',label='部门名称',max_length=10)
    class Meta:
        model=Employee
        fields = ['empid', 'name', 'title','real_salary','depname']
    def get_real_salary(self, obj):
        return obj.salary.basesalary + obj.salary.titlesalary - obj.salary.deduction
#第11题
class EmployeeTitleInfoSerializer(serializers.ModelSerializer):
    title_num=serializers.IntegerField(label='职称人数')
    class Meta:
        model=Employee
        fields=['title','title_num']

#第12题
class DepSalarySerializer(serializers.Serializer):
    salary_sum = serializers.IntegerField(label='实发工资总和')
    salary_avg = serializers.IntegerField(label='实发工资平均')
    depname=serializers.CharField(label='部门名称',max_length=10,source='department__depname')

#第13题
class EmpolyeeNameSerializer(serializers.Serializer):
    name=serializers.CharField(label='员工姓名',max_length=10)
# {
#     name:'工程师',
#     num:2
# }

class PhoneTokenRefreshSerializer(TokenObtainPairSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[self.username_field] = serializers.CharField()
        self.fields['phone_code'] = serializers.IntegerField()
        del self.fields['password']
    def validate_phone_code(self, value):
        cache_code=cache.get(Users.objects.filter(username=self.initial_data['username'])[0].phone)
        if cache_code!=value:
            raise serializers.ValidationError('验证码错误！',code='code_error')
        return value
    def validate(self, attrs):
        self.user=Users.objects.get(username=self.initial_data['username'])
        refresh = self.get_token(self.user)
        data={}
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        return data

class PhoneUserNameSerializer(serializers.Serializer):
    username=serializers.CharField(label='登录名',max_length=10)
    def validate_username(self, value):
        result=Users.objects.filter(username=value)
        if result is None:
            raise serializers.ValidationError('用户未注册！',code='no_register')
        return result[0].phone

class AreaProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model=AreaCity
        fields=['area_name','id']