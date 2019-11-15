from django.urls import path
from . import views

app_name = 'wechat'

urlpatterns = [
    path(r'^$', views.wechat_main, name='wechat_main'),
]