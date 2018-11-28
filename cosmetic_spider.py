from random import randint
from time import sleep
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

url = 'http://www.hengjietong.com/productSystem/index.php?tag=X*TgZbDSX(UDRcS'

def get_html(url, retry_time=5):
    headers = {
            'User-Agent': "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Mobile Safari/537.36"
            }
    try:
        session = requests.Session()
        wb_data = session.get(
                    url, 
                    headers=headers, 
                    timeout=10, 
                    cookies={
                        'PHPSESSID': 'tb1603iaen3a6nb7ejkgk8f900',
                        'td_cookie': '1839250161',
                    })      # cookies获取授权码
        bsobj = BeautifulSoup(wb_data.text, 'lxml')
        return bsobj
    except:
        if retry_time > 0:
            return get_html(url, retry_time - 1)
        else:
            print('数据获取失败')
            raise

def get_item_information(bsobj):
    data_set = []
    item_name = bsobj.select('#product > tbody > tr > td.td_header_name')
    item_count = bsobj.select('#product > tbody > tr > td.td_header_count')
    # original_price = bsobj.select('#product > tbody > tr > td.td_header_price')
    for name, count in zip(item_name, item_count):
        data = {
            'item_name': name.get_text(),
            'item_count': count.get_text(),
        }
        data_set.append(data)
    return data_set

def get_status(bsobj):
    update_time = bsobj.select('body > div > p')
    status = {
        'update_time': update_time[0].get_text().split('：')[1],
        'status': '正常',
        'sign': 0
    }
    return status


if __name__ =='__main__':
    client = MongoClient('localhost', 27017)    # 定义MongoDB client
    cosmetic = client['COSMETIC_DATA']          # 定义数据库对象
    original_sheet = cosmetic['ORIGINAL_SHEET'] # 定义表ORIGINAL_SHEET对象
    status = cosmetic['STATUS']                 # 定义表STATUS对象
    status.drop()
    try:
        bsobj = get_html(url)                       # 获得BeautifulSoup object
        if original_sheet is not None:
            original_sheet.drop()
        data_set = get_item_information(bsobj)
        for data in data_set:
            original_sheet.insert_one(data)

        status_data = get_status(bsobj)
        status.insert_one(status_data)
    except:
        print('数据获取异常')
        args = {'$set': {'update_time': '','status':'数据获取失败，请联系管理员','sign':0}}
        status.insert_one(args)