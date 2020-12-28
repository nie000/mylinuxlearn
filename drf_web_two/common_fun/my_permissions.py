


#权限是针对已登录的用户
from rest_framework import permissions
from rest_framework.request import Request


class MyPermiss(permissions.BasePermission):
    message="咩有权限！"
    def has_permission(self, request:Request, view):
        if request.user.is_admin:
            return True
        else:
            return False

class NomalPermiss(permissions.BasePermission):
    """普通用户权限"""
    message = '权限不够！！！'
    role=0
    def has_permission(self, request, view):  #对于列表的访问权限
        if request.user.role>=self.role:
            return True
        else:
            return False
    def has_object_permission(self, request, view, obj):  #对于对象的访问权限
        return self.has_permission(request,view)

class RootPermiss(NomalPermiss):
    """管理员权限"""
    message = '需要vip权限！！！'
    role=1