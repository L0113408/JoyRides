
import random
from typing import List

import requests
import json
import numpy as np
import base64
import os
import cv2

from user import User

from PIL import Image
from wechaty import (
    Message,
    Contact
)

with open('./data/config.json', 'r') as f:
    config = json.load(f)
with open('./data/data.json', 'r') as f:
    processes = json.load(f)
names_CN = processes['names_CN']

def cv2_to_base64(image):
    data = cv2.imencode('.jpg', image)[1]
    return base64.b64encode(data.tostring()).decode('utf8')


def base64_to_cv2(b64str):
    data = base64.b64decode(b64str.encode('utf8'))
    data = np.fromstring(data, np.uint8)
    data = cv2.imdecode(data, cv2.IMREAD_COLOR)
    return data

#在图片上绘制一个框，返回问题答案
def plot_one_box(x, img, color=None, label=None, line_thickness=None):
    # Plots one bounding box on image img
    tl = line_thickness or round(0.002 * (img.shape[0] + img.shape[1]) / 2) + 1  # line/font thickness
    color = color or [random.randint(0, 255) for _ in range(3)]
    c1, c2 = (int(x[0]-x[2]/2), int(x[1]-x[3]/2)), (int(x[0]+x[2]/2), int(x[1]+x[3]/2))
    cv2.rectangle(img, c1, c2, color, thickness=tl, lineType=cv2.LINE_AA)
    if label:
        tf = max(tl - 1, 1)  # font thickness
        t_size = cv2.getTextSize(label, 0, fontScale=tl / 3, thickness=tf)[0]
        c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3
        cv2.rectangle(img, c1, c2, color, -1, cv2.LINE_AA)  # filled
        cv2.putText(img, label, (c1[0], c1[1] - 2), 0, tl / 3, [225, 255, 255], thickness=tf, lineType=cv2.LINE_AA)

class Action(object):
    def __init__(self, msg: Message):
        self.msg = msg

    # 多分支路径选择
    def Switch(self, user_Info : User):
        path = r''
        # 回复消息文本
        text: str = self.msg.text()
        # 获取状态信息
        cur_Process = processes[user_Info.state]
        if text in cur_Process :
            # 根据回复选择路径分支
            user_Info.state = cur_Process[text]['next']
            cur_Process = processes[user_Info.state]
            send = cur_Process['question']
        else :
            send = None
        return send, user_Info

    # 选择处理类型
    def SwitchType(self, user_Info : User):
        path = r''
        text: str = self.msg.text()
        cur_Process = processes[user_Info.state]
        if text in cur_Process :
            #user_Info.qstntype = cur_Process[text]['type']
            user_Info.state = cur_Process['A00']['next']
            cur_Process = processes[user_Info.state]
            send = cur_Process['question']
        else :
            send = None
        return send, user_Info

    # 发送消息
    def SendMsg(self, user_Info : User):
        cur_Process = processes[user_Info.state]
        user_Info.state = cur_Process['A00']['next']
        cur_Process = processes[user_Info.state]
        send = cur_Process['question']
        return send, user_Info

    # 接受图片
    def RivcePic(self, user_Info : User):
        #img_path = ''
        cur_Process = processes[user_Info.state]
        if 'imgpath' in cur_Process :
            img_path  = cur_Process['imgpath']
            user_Info.state = cur_Process['A00']['next']
            cur_Process = processes[user_Info.state]
            send = cur_Process['question']
        else :
            send = None
        return send, user_Info

    # 接受图片
    def SaveUserImage(self, user_Info : User):
        #img_path = ''
        cur_Process = processes[user_Info.state]
        from_contact : Contact = self.msg.talker()
        # if self.msg.wechaty.contact_id == from_contact.contact_id :  return
        datafile : str = './DataBase/user/{}.json'.format(from_contact.contact_id)
        
        if os.path.exists(datafile) :
            pass
        # else :
        #     json.dump(config, f)
        if 'imgpath' in cur_Process :
            img_path  = cur_Process['imgpath']
            user_Info.state = cur_Process['A00']['next']
            cur_Process = processes[user_Info.state]
            send = cur_Process['question']
        else :
            send = None
        return send, user_Info

    # 发送图片
    def SendPic(self, user_Info : User):
        cur_Process = processes[user_Info.state]
        if 'imgpath' in cur_Process :
            img_path  = cur_Process['imgpath']
            if img_path == '{User}' :
                img_path = user_Info.imgpath
            #send = cur_Process['question']
            user_Info.state = cur_Process['A00']['next']
            cur_Process = processes[user_Info.state]
            send = "imgpath|{0}".format(img_path)
        else :
            send = None
        return send, user_Info

    # 发送系统图片
    def SendSysPic(self, user_Info : User):
        cur_Process = processes[user_Info.state]
        img_path = r'./images/street'
        if 'imgpath' in cur_Process :
            img_path  = cur_Process['imgpath']
        flielist = os.listdir(img_path)
        
        if len(flielist) > 1 :
            num = random.randrange(len(flielist))
            # img_path = os.path.join(img_path, flielist[num])
            img_path = '{}/{}'.format(img_path, flielist[num])
            user_Info.imgpath = img_path
            #send = cur_Process['question']
            user_Info.state = cur_Process['A00']['next']
            cur_Process = processes[user_Info.state]
            send = "imgpath|{0}".format(img_path)
        else :
            send = None
        return send, user_Info

    # 发送链接
    def SendUrl(self, user_Info : User):
        cur_Process = processes[user_Info.state]
        if 'imgpath' in cur_Process :
            img_path  = cur_Process['imgpath']
            #send = cur_Process['question']
            user_Info.state = cur_Process['A00']['next']
            cur_Process = processes[user_Info.state]
            #send = FileBox.from_url(img_path)
            send = "url|{0}".format(img_path)
        else :
            send = None
        return send, user_Info

    # 正误判断
    def Check(self, user_Info : User):
        cur_Process = processes[user_Info.state]
        cls = user_Info.cls
        object = processes['objects'][cls[1]]
        text: str = self.msg.text()
        if "答案" == text :
            send = "imgpath|{0}".format(user_Info.imgpath)
            return send, user_Info

        '''
        for c in text:
            a = (ord(c) - ord('0'))
            if (a > 0) and (a < 9) : ret = (ret * 10) + a
            '''

        user_Info.state = cur_Process['A00']['next']
        #if (object['name'] in text) and (str(cls[2]) in text) :
        if (str(cls[2]) in text) :
            send = processes['right']['question']
            user_Info.state = 'P99'
        else :
            send = processes['wrong']['question']
        return send, user_Info
    
    # 图片分割/绘画
    def facade(self, user_Info : User):
        cur_Process = processes[user_Info.state]
        # img_path : str = cur_Process['imgpath']
        img_path : str = user_Info.imgpath

        # org_im是主动发送的原图，通过机器人接收存在服务器
        org_im = cv2.imread(img_path)  # 替换1.jpg为变量
        
        x, y = org_im.shape[0:2]

        org_im = cv2.resize(org_im, ( 704,480))
        data = {'image': cv2_to_base64(org_im)}   

        # 请求链接
        # apikey就是应用key
        url = "https://aistudio.baidu.com/serving/online/6716?apiKey=95564e53-5804-4e51-bd8d-c1a035eb36c4"
        # 发送HTTP请求
        r = requests.post(url=url, data=json.dumps(data))
        print(r)
        print(r.json())
        # base64处理后的数据
        base64_img = r.json()['result']['image']
        # 自定义保存文件名
        #target_img = os.path.join('target_img', 'target_img' + img_path.split('/')[-1])
        target_img = img_path.replace('input', 'output', 1)
        with open(target_img, 'wb+') as f:  # test.jpg可自定义，后面 robot 返回给用户
            f.write(base64.b64decode(base64_img.split(',')[-1]))

        user_Info.imgpath = target_img
        user_Info.state = cur_Process['A00']['next']
        cur_Process = processes[user_Info.state]
        send = "imgpath|{0}".format(target_img)
        return send, user_Info


    # 看图问答
    def Count(self, user_Info : User):
        # names_CN = processes['objects']
        cur_Process = processes[user_Info.state]
        # img_path : str = cur_Process['imgpath']
        img_path : str = user_Info.imgpath
        imageName : str = img_path
        strlist = img_path.split('/')
        if len(strlist) >1 :
            imageName = strlist[-1]

        file = open(img_path, mode='rb')
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            "Connection": "keep-alive",
            "Host": "36kr.com/newsflashes",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:55.0) Gecko/20100101 Firefox/55.0"
        }

        index  = strlist[-1].rindex('.')
        files = {'file': (f'{strlist[-1][:index]}', file, 'image/jpg')}
        print('向服务器发送请求！')
        # url = 'http://124.114.22.149:20051/api'
        url = 'http://124.114.22.21:20051/api'
        # url = 'http://192.168.1.200:5001/api'
        # url = 'http://127.0.0.1:5000/api'
        re = requests.post(url,headers,files=files)
        if re.status_code == 200:
            data = json.loads(re.content)
            imgName = data['imageName']
            boxList = data['resJson']
            clsList = data['resCls']

            img = Image.open(img_path)
            imgArray = np.array(img)
            txt_path = f'./DataBase/boxList/{imgName}'
            # 收到boxList，绘制
            for eachbox in boxList:
                label2 = f"{names_CN[f'{eachbox[-2]}']} {eachbox[-1]*100}"
                label = '%s %.2f%%' % (eachbox[-2], eachbox[-1]*100)
                print(label2)
                plot_one_box(eachbox, imgArray, label=label, color=None, line_thickness=3)
            img = Image.fromarray(imgArray)
            # img.show()

            img_path = f'./DataBase/image/{imgName}.jpg'

            img.save(f'./DataBase/image/{imgName}.jpg')

            user_Info.imgpath = img_path

            if len(clsList) > 1 :
                num = random.randrange(len(clsList))
                user_Info.cls = clsList[num]
                send = f"图片中{names_CN[f'{clsList[num][1]}']}数量是多少呢?"
                user_Info.state = cur_Process['A00']['next']
            else :
                send = '没有能成功识别，请重新开始。。。'
                user_Info.state = 'P98'
                cur_Process = processes[user_Info.state]
                send = cur_Process['question']
            # await msg.say(question)
        else:
            # await  msg.say(f"编号{str(imagesList[-1])[:-4]}图片正在飞速发往图片星球路上被加勒比星球拦截，请重新发送！...")
            send = '图片识别失败，请重新发送！……'
            user_Info.state = 'P20'
        return send, user_Info
