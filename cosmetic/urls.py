from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),    # cosmetic应用默认页，无后缀
    path('search/',  views.search, name='search')
]