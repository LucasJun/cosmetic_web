from django.shortcuts import render     # render是Django提供的捷径
from cosmetic.models import ItemInfo    # 连接models.py


def index(request):
    itemInfo = ItemInfo.objects # object方法返回结构化数据

    context = {
        'itemInfo': itemInfo,
    }
    return render(request, 'all_item.html', context=context)  # 把model模块定义的数据结构接入页面中


def search(request):
    request.encoding = 'utf-8'              # 接收input编码
    index_data = request.GET['search']      # 获取search请求数据
    itemInfo = ItemInfo.objects(title__icontains=index_data)    # mongoengine提供的检索方法，返回object对象
    context = {
        'itemInfo': itemInfo,
    }
    return render(request, 'search_result.html', context=context)