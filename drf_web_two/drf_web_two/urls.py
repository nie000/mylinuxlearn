"""drf_web_two URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.static import serve
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from drf_web_two.settings.base_settings import MEDIA_ROOT, STATIC_DIR
from systems_mgr.views import PhoneTokenObtainPairView

schema_view = get_schema_view(
    openapi.Info(
        title="RIMI API",  # 在线文档标题
        default_version='v1',  # 在线文档版本
        description="Test description",  # 在线文档描述
        terms_of_service="https://www.google.com/policies/terms/",  # 服务团队地址
        contact=openapi.Contact(email="contact@snippets.local"),  # 邮箱联系
        license=openapi.License(name="BSD License"),  # 许可条款
    ),
    public=True,  # 是否是公共访问
    permission_classes=(permissions.AllowAny,),  # ?
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('systems_mgr/',include('systems_mgr.urls')),
    re_path(r'^api/token/$', TokenObtainPairView.as_view(), name='token_obtain_pair'),#
    re_path(r'^api/phone_token/$', PhoneTokenObtainPairView.as_view(), name='phone_token_obtain_pair'),#
    re_path(r'^api/token/refresh/$', TokenRefreshView.as_view(), name='token_refresh'),  #
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0),name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0),name='schema-redoc'),
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root':MEDIA_ROOT}),
re_path(r'^static/(?P<path>.*)$', serve, {'document_root':STATIC_DIR}),
]
