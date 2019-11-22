from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),    # membership应用默认页，无后缀
    path('table/', views.table, name='table'),
    path('table/record', views.record, name='record'),
    # path('result/', views.result, name='result'),
    path('login/', views.login, name='login'),
]