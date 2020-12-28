from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models

# Create your models here.
class MyUserManager(BaseUserManager):
    def create_superuser(self, username, name, card_id,password,card_type,auth_type,sex,email):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.model(
            username=username,
            name=name,
            password=password,
            card_id=card_id,
            card_type=card_type,
            auth_type=auth_type,
            sex=sex,
            email=email
        )
        user.is_admin = True
        user.set_password(password)
        user.save(using=self._db)
        return user


class Users(AbstractBaseUser):
    sex_list = (
        (0, '女'),
        (1, '男')
    )
    card_list = (
        (0, '内地居民身份证'),
        (1, '港澳居民身份证'),
        (2, '护照')
    )
    auth_list = (
        (0, '手机'),
        (1, '邮箱')
    )
    role_list=(
        (0,'普通用户'),
        (1,'vip')
    )
    username = models.CharField('登录名', max_length=20, unique=True)
    name = models.CharField(verbose_name='真实姓名', max_length=10)
    card_type = models.SmallIntegerField('证件类型', choices=card_list)
    card_id = models.CharField('证件号码', max_length=20)
    password = models.CharField('密码', max_length=128)
    auth_type = models.SmallIntegerField('验证方式', choices=auth_list)
    age = models.IntegerField('年龄', null=True, blank=True)
    sex = models.SmallIntegerField('性别', choices=sex_list, default=0)
    phone = models.CharField('电话', max_length=11, unique=True, null=True, blank=True)
    email = models.EmailField('邮箱')
    create_datetime = models.DateTimeField('创建时间', auto_now_add=True)
    update_datetime = models.DateTimeField('更新时间', auto_now=True)
    user_img = models.ImageField(upload_to='user_img/', verbose_name='用户头像', null=True, blank=True)

    is_active = models.BooleanField('账户是否激活', default=True)
    is_admin = models.BooleanField('账户是否后台管理员', default=False)
    role=models.SmallIntegerField('账户角色',choices=role_list,default=0)
    objects = MyUserManager()

    USERNAME_FIELD = 'username'  # 登录字段
    REQUIRED_FIELDS = ['name', 'card_id', 'password', 'card_type', 'auth_type', 'sex', 'email']  # 注册必填字段

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes,
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    class Meta:
        verbose_name_plural='用户信息'
from django.db import models

# Create your models here.
class ApiMgr(models.Model):
    btn_list=(
        (0,'del'),
        (1,'add'),
        (2,'upd')
    )
    type_list=(
        (0,'POST'),
        (1,'GET')
    )
    api_name=models.CharField('服务名称',max_length=10)
    api_url = models.CharField('服务路由', max_length=20)
    api_type = models.SmallIntegerField('服务类型', choices=type_list)
    source = models.CharField('服务模块', max_length=10)
    btn = models.SmallIntegerField('服务权限', choices=btn_list)
    is_delete=models.SmallIntegerField('是否已删除',default=0)

class Comment(models.Model):
    email = models.EmailField('邮箱')
    content = models.CharField('内容',max_length=255)
    created = models.DateTimeField(auto_now_add=True)

class Grade(models.Model):
    name=models.CharField('班级名称',max_length=10)
    max_student=models.SmallIntegerField('班级容纳最大人数')
    def __str__(self):
        return self.name

class Teacher(models.Model):
    name=models.CharField('老师姓名',max_length=10)
    grade=models.ManyToManyField(Grade)
    def __str__(self):
        return self.name


class Student(models.Model):
    name = models.CharField('学生姓名', max_length=20)
    age = models.SmallIntegerField('年龄')
    birthday = models.DateField('生日')
    grade = models.ForeignKey(Grade, verbose_name='所属班级', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class Salary(models.Model):
    basesalary = models.IntegerField('基本工资')
    titlesalary = models.IntegerField('职务工资')
    deduction = models.IntegerField('扣除工资')


class Department(models.Model):
    depid=models.AutoField('部门编号',primary_key=True)
    depname=models.CharField('部门名称',max_length=10)
    # descripations=RichTextField('部门简介',blank=True,null=True)
    descripations = RichTextUploadingField('部门简介', blank=True, null=True)

    # descripations=models.CharField('部门简介',max_length=255,null=True,blank=True)
class AreaCity(models.Model):
    type_list=(
        (1,'省'),
        (2,'市'),
        (3,'区/县')
    )
    area_name=models.CharField('区域名称',max_length=20)
    area_type=models.SmallIntegerField('区域类型',choices=type_list)
    area_sort=models.SmallIntegerField('排序',default=0)
    area_parent=models.ForeignKey('self',on_delete=models.SET_NULL,null=True)
class Employee(models.Model):
    sex_list=(
        (0,'女'),
        (1,'男')
    )
    empid=models.AutoField('雇员编号',primary_key=True)
    name=models.CharField('姓名',max_length=20)
    sex=models.SmallIntegerField('性别',choices=sex_list)
    title=models.CharField('职称',max_length=10)
    birthday=models.DateField('出生日期')
    department=models.ForeignKey(Department,on_delete=models.SET_NULL,null=True)
    salary=models.OneToOneField(Salary,on_delete=models.SET_NULL,null=True)
    address=models.ForeignKey(AreaCity,on_delete=models.SET_NULL,null=True)

