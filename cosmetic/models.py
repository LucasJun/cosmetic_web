# from django.db import models    # 未使用Django自带的参数，Django默认使用sqlite
from mongoengine import *   # 防止名称冲突可单独import需要的类


class ItemInfo(Document):   # 继承mongoengine自带的Document类
    # 定义数据结构，此处命名要和数据库种变量名一致
    item_name = StringField()
    item_count = StringField()
    item_price = StringField()
    date = StringField()
    # original_price = StringField()    # 不显示价格
    # 数据库元参数
    meta = {
            'collection':'PRODUCT_SHEET',  # 指定数据库中的表（sheet）
            }

# class ListStatus(Document):    # 列表更新状态
#     update_time = StringField()
#     status = StringField()
#     sign = IntField()
#     meta = {
#         'collection': 'STATUS',
#     }
