import hashlib
import json
from django.utils.encoding import smart_str
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse


def wechat_main(request):
    if request.method == 'GET':
        signature = request.GET.get('signature', None)
        timestamp = request.GET.get('timestamp', None)
        nonce = request.GET.get('nonce', None)
        echostr = request.GET.get('echostr', None)

        token = 'random_code'

        hashlist = [token, timestamp, nonce]
        hashlist.sort()
        hashstr = ''.join([s for s in hashlist])
        hashstr = hashlib.sha1(hashstr).hexdigest()
        if hashstr == signature:
          return HttpResponse(echostr)
        else:
          return HttpResponse("field")
    else:
        othercontent = autoreply(request)
        return HttpResponse(othercontent)

#微信服务器推送消息是xml的，根据利用ElementTree来解析出的不同xml内容返回不同的回复信息，就实现了基本的自动回复功能了，也可以按照需求用其他的XML解析方法
import xml.etree.ElementTree as ET

def autoreply(request):
    # try:
    webData = request.body
    xmlData = ET.fromstring(webData)

    msg_type = xmlData.find('MsgType').text
    ToUserName = xmlData.find('ToUserName').text
    FromUserName = xmlData.find('FromUserName').text
    CreateTime = xmlData.find('CreateTime').text
    MsgType = xmlData.find('MsgType').text
    MsgId = xmlData.find('MsgId').text

    toUser = FromUserName
    fromUser = ToUserName

    if msg_type == 'text':
        content = "您好,感谢您成为会员!"
        replyMsg = TextMsg(toUser, fromUser, content)
        print(replyMsg) 
        return replyMsg.send()
    else:
        msg_type == 'link'
        content = "您输入的内容无法识别~"
        replyMsg = TextMsg(toUser, fromUser, content)
        return replyMsg.send()            

        # elif msg_type == 'image':
        #     content = "图片已收到,谢谢"
        #     replyMsg = TextMsg(toUser, fromUser, content)
        #     return replyMsg.send()
        # elif msg_type == 'voice':
        #     content = "语音已收到,谢谢"
        #     replyMsg = TextMsg(toUser, fromUser, content)
        #     return replyMsg.send()
        # elif msg_type == 'video':
        #     content = "视频已收到,谢谢"
        #     replyMsg = TextMsg(toUser, fromUser, content)
        #     return replyMsg.send()
        # elif msg_type == 'shortvideo':
        #     content = "小视频已收到,谢谢"
        #     replyMsg = TextMsg(toUser, fromUser, content)
        #     return replyMsg.send()
        # elif msg_type == 'location':
        #     content = "位置已收到,谢谢"
        #     replyMsg = TextMsg(toUser, fromUser, content)
        #     return replyMsg.send()
    # except Exception, Argment:
    #     return Argment

class Msg(object):
    def __init__(self, xmlData):
        self.ToUserName = xmlData.find('ToUserName').text
        self.FromUserName = xmlData.find('FromUserName').text
        self.CreateTime = xmlData.find('CreateTime').text
        self.MsgType = xmlData.find('MsgType').text
        self.MsgId = xmlData.find('MsgId').text

import time
class TextMsg(Msg):
    def __init__(self, toUserName, fromUserName, content):
        self.__dict = dict()
        self.__dict['ToUserName'] = toUserName
        self.__dict['FromUserName'] = fromUserName
        self.__dict['CreateTime'] = int(time.time())
        self.__dict['Content'] = content

    def send(self):
        XmlForm = """
        <xml>
        <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
        <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
        <CreateTime>{CreateTime}</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[{Content}]]></Content>
        </xml>
        """
        return XmlForm.format(**self.__dict)