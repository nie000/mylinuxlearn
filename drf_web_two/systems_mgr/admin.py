from django.contrib import admin

# Register your models here.
from systems_mgr.models import Users, Department

admin.site.site_header = '聂总跨国商超管理平台'  # 设置标题
admin.site.site_title = '聂总跨国商超管理平台'  # 设置标题

@admin.register(Users)
class AuthorAdmin(admin.ModelAdmin):
    list_per_page = 10      # list_per_page设置每页显示多少条记录，默认是100条
    ordering = ('-last_login',)     # ordering设置默认排序字段，负号表示降序排序

    list_display = ('id', 'username', 'name', 'phone',  'email', 'last_login')     # list_display设置要显示在列表中的字段（id字段是Django模型的默认主键）
    list_display_links = ('id', 'username')     # 设置哪些字段可以点击进入编辑界面

    list_filter = ('card_type', 'sex')  # 过滤器
    search_fields = ('username',)  # 搜索字段

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('depname','depid')