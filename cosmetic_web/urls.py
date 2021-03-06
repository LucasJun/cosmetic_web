"""cosmetic_web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, include

urlpatterns = [
    path('cosmetic/', include('cosmetic.urls')),    # 添加cosmetic/作为网站应用入口，应用urls指向cosmetic.urls
    path('admin/', admin.site.urls),    # admin为管理员应用入口，Django默认开启
    path('wx/', include('wechat.urls',namespace='wechat')),
    path('membership/', include('membership.urls')),
]
