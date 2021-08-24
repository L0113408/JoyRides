"""
Python Wechaty - https://github.com/wechaty/python-wechaty
Authors:    Huan LI (李卓桓) <https://github.com/huan>
            Jingjing WU (吴京京) <https://github.com/wj-Mcat>
2020 @ Copyright Wechaty Contributors <https://github.com/wechaty>
Licensed under the Apache License, Version 2.0 (the 'License');
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an 'AS IS' BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

#from asyncio.windows_events import NULL
import os
import asyncio
import json
import array
#import paddlehub as hub
#import cv2
#from PIL import Image
from operator import methodcaller

#from wechaty.user import room

from user import User
from action import Action
#from typing import Union
#from wechaty.plugin import WechatyPlugin
from wechaty import (
    Contact,
    Room,
    FileBox,
    Message,
    Wechaty,
    ScanStatus,
    user,
)

with open('./data/data.json', 'r') as f:
    processes = json.load(f)
with open('./data/pair.json', 'r') as f:
    pair = json.load(f)


statkey = '出发吧'
#ninghtkey = '黑夜模式'
ninghtkey = '天黑了'
curProcess = ''
userInfo : User
userInfo = ''
dicuser = {}

#model = hub.Module(name="humanseg_lite")
os.environ['WECHATY_PUPPET']="wechaty-puppet-service"
#os.environ['WECHATY_PUPPET_SERVICE_TOKEN']="puppet_padlocal_ef80ab0ab8f547c39b0b2460fb1f3027"
# os.environ['WECHATY_PUPPET_SERVICE_TOKEN']="puppet_padlocal_44f190e6ea6845558fcb3cfdf70d8a59"
# os.environ['WECHATY_PUPPET_SERVICE_ENDPOINT']="182.61.61.97:8080"

os.environ['WECHATY_PUPPET_SERVICE_TOKEN']='puppet_padlocal_6c909d60a7444eeaa106e044de0a6026'
os.environ['WECHATY_PUPPET_SERVICE_ENDPOINT']="106.13.69.114:8080"

#os.environ['WECHATY_PUPPET_SERVICE_TOKEN']='puppet_padlocal_6c909d60a7444eeaa106e044de0a6026'
#os.environ['WECHATY_PUPPET_SERVICE_ENDPOINT']="106.13.69.114:8080"

class DoProcess(object):
    def __init__(self, msg: Message):
        self.msg = msg


    # 唤醒
    def S01(self, user_Info : User):
        cur_Process = processes[processes['start']]
        send = cur_Process['question']
        from_contact = self.msg.talker()
        room = self.msg.room()
        user_Info = User(from_contact.contact_id)
        user_Info.contact = from_contact
        user_Info.room = None
        if room is not None :
            user_Info.roomtopic = room.room_id
            user_Info.room = room
        user_Info.state = cur_Process['state']
        return send, user_Info
        
    def P01(self, user_Info : User):
        a = Action(self.msg)
        cur_Process = processes[user_Info.state]
        method = cur_Process['action']
        result = methodcaller(method, user_Info)(a) 
        return result

    # 拍照模式
    def P02(self, user_Info : User):
        from_contact = self.msg.talker()
        if self.msg.wechaty.contact_id == from_contact.contact_id :  return
        
        a = Action(self.msg)
        cur_Process = processes[user_Info.state]
        method = cur_Process['action']
        result = methodcaller(method, user_Info)(a)   
       # send = self["A00"]
        return result

    # 接受图片
    def P03(self, user_Info : User):
        a = Action(self.msg)
        cur_Process = processes[user_Info.state]
        method = cur_Process['action']
        result = methodcaller(method, user_Info)(a)
        return result

    # 系统发送图片
    def P04(self, user_Info : User):
        a = Action(self.msg)
        cur_Process = processes[user_Info.state]
        method = cur_Process['action']
        result = methodcaller(method, user_Info)(a)
        if result[0] is not None:
            send = result[0]
            user_Info : User = result[1]
            params = send.split('|')
            if len(params) > 1 :
                if params[0] == 'imgpath' :
                    user_Info.imgpath =  params[1]                    
        return result

    # TODO
    def P05(self, user_Info : User):
        a = Action(self.msg)
        cur_Process = processes[user_Info.state]
        method = cur_Process['action']
        result = methodcaller(method, user_Info)(a)
        return result

    # 选择交互模式
    def P06(self, user_Info : User):
        a = Action(self.msg)
        cur_Process = processes[user_Info.state]
        text: str = self.msg.text()
        if text in cur_Process :
            user_Info.qstntype = cur_Process[text]['type']
        method = cur_Process['action']
        user_Info.cls = None
        result = methodcaller(method, user_Info)(a)  
        return result

    # 选择图片来源
    def P07(self, user_Info : User):
        a = Action(self.msg)
        cur_Process = processes[user_Info.state]
        #text: str = self.msg.text()
        #if text in cur_Process :
       #     user_Info.chose = cur_Process[text]['type']
        method = cur_Process['action']
        result = methodcaller(method, user_Info)(a)  
        return result

    # 绘画流程入口
    def P10(self, user_Info : User):
        a = Action(self.msg)
        cur_Process = processes[user_Info.state]
        #text: str = self.msg.text()
        #if text in cur_Process :
       #     user_Info.chose = cur_Process[text]['type']
        method = cur_Process['action']
        result = methodcaller(method, user_Info)(a)  
        return result

    # 系统发送图片
    def P11(self, user_Info : User):
        a = Action(self.msg)
        cur_Process = processes[user_Info.state]
        method = cur_Process['action']
        result = methodcaller(method, user_Info)(a)
        return result

    # 接受图片
    def P12(self, user_Info : User):
        from_contact = self.msg.talker()
        if self.msg.wechaty.contact_id == from_contact.contact_id :  return
        a = Action(self.msg)
        cur_Process = processes[user_Info.state]
        method = cur_Process['action']
        result = methodcaller(method, user_Info)(a)
        return result

    # 接受图片
    def P15(self, user_Info : User):
        a = Action(self.msg)
        cur_Process = processes[user_Info.state]
        method = cur_Process['action']
        result = methodcaller(method, user_Info)(a)
        return result

    # TODO
    def P05(self, user_Info : User):
        a = Action(self.msg)
        cur_Process = processes[user_Info.state]
        method = cur_Process['action']
        result = methodcaller(method, user_Info)(a)
        return result

    # 绘画流程入口
    def P20(self, user_Info : User):
        # from_contact = self.msg.talker()
        # if self.msg.wechaty.contact_id == from_contact.contact_id :  return
        a = Action(self.msg)
        cur_Process = processes[user_Info.state]

        method = cur_Process['action']
        result = methodcaller(method, user_Info)(a)  
        return result

    # 比较答案
    def P21(self, user_Info : User):
        from_contact = self.msg.talker()
        if self.msg.wechaty.contact_id == from_contact.contact_id :  return
        a = Action(self.msg)
        cur_Process = processes[user_Info.state]
        method = cur_Process['action']
        result = methodcaller(method, user_Info)(a)
        return result

    # 接受图片
    def P22(self, user_Info : User):
        a = Action(self.msg)
        cur_Process = processes[user_Info.state]
        method = cur_Process['action']
        result = methodcaller(method, user_Info)(a)
        return result

    # TODO
    def P05(self, user_Info : User):
        a = Action(self.msg)
        cur_Process = processes[user_Info.state]
        method = cur_Process['action']
        result = methodcaller(method, user_Info)(a)
        return result

    def P90(self, user_Info : User):
        a = Action(self.msg)
        from_contact = self.msg.talker()
        user_Info = User(from_contact.contact_id)
        user_Info.state = 'P90' 
        cur_Process = processes['P90']
        method = cur_Process['action']
        result = methodcaller(method, user_Info)(a)  
        return result

    # 选择图片来源
    def P98(self, user_Info : User):
        a = Action(self.msg)
        cur_Process = processes[user_Info.state]
        #text: str = self.msg.text()
        #if text in cur_Process :
       #     user_Info.chose = cur_Process[text]['type']
        method = cur_Process['action']
        result = methodcaller(method, user_Info)(a)  
        return result

    def P99(self, user_Info : User):
        a = Action(self.msg)
        cur_Process = processes[user_Info.state]
        method = cur_Process['action']
        result = methodcaller(method, user_Info)(a)  
        return result

def doGame(msg: Message, img_path: str):
    global userInfo
    global curProcess
    result = None
    #if msg.text() == 'show the game':  
    if msg.text() == ninghtkey:
        # 流程唤醒
        dp =  DoProcess(msg)
       # userInfo.state = 'P90'
        result = methodcaller('P90', userInfo)(dp) 
    elif msg.text() == statkey:
        # 流程唤醒
        dp =  DoProcess(msg)
        result = methodcaller('S01', userInfo)(dp) 
    elif userInfo:
        dp =  DoProcess(msg)        
        curProcess = processes[userInfo.state]
        # if 'imgpath' in curProcess :
        #     curProcess['imgpath'] = img_path
        if img_path is not None :
            userInfo.imgpath = img_path
        result = methodcaller(curProcess['state'], userInfo)(dp)
        #userInfo.state = result[1]
        #userInfo.type = 

    if (result is not None) and (len(result) > 1) :
        userInfo = result[1]
        return result
    else :
        return ''

async def save_img(msg: Message):
    # 将Message转换为FileBox
    file_box_2 = await msg.to_file_box()
    # 获取图片名
    img_name = file_box_2.name
    # 图片保存的路径
    img_path = './images/input/' + img_name
    # 将图片保存为本地文件
    await file_box_2.to_file(file_path=img_path)
    return img_path

command = ['0','1','2', statkey, ninghtkey, processes['P03']['question'], processes['P04']['question']]

async def on_message(msg: Message):
    global contact
    from_contact = msg.talker()
    # room = msg.room()
    # msg.wechaty.contact_id
   # if from_contact.is_self :  return

   # text = msg.text()
   #conversation: Union[Room, Contact] = from_contact if room is None else room
   # await conversation.ready()
    #await conversation.say('dong')
    img_path = None
    # 如果收到的message是一张图片
    
    if msg.type() == Message.Type.MESSAGE_TYPE_IMAGE:
        from_contact = msg.talker()
        if msg.wechaty.contact_id != from_contact.contact_id :  
        # img_path = './image/3330.jpeg'
       # '''
            # 将Message转换为FileBox
            file_box_2 = await msg.to_file_box()
            # 获取图片名
            img_name = file_box_2.name
            # 图片保存的路径
            img_path = './images/input/' + img_name
            #img_path = img_name
            print('img_path=', img_path)
            # 将图片保存为本地文件
            await file_box_2.to_file(file_path=img_path)
       # '''
    # 游戏流程处理
    isCommand = False
   # if (msg.text() in command) or (img_path is not None) :
    #    isCommand = True
    #while isCommand :
    if True :
        result = doGame(msg, img_path = img_path) 
        
        if len(result) > 1 :
            if result[0] is not None:
                send = result[0]
                user_Info : User = result[1]
                params = send.split('|')
                if len(params) > 1 :
                    if params[0] == 'imgpath' :
                        #file_box_3 = params[1]
                        file_box_3 = FileBox.from_file(params[1])
                        await msg.say(file_box_3) 
                        send = None
                    if params[0] == 'url' :
                        file_box_3 = params[1]
                        #file_box_3 = FileBox.from_url(params[1], '黑夜模式')
                        await msg.say(file_box_3) 
                        send = None


                if send is not None:
                    if user_Info.room is not None :
                        await user_Info.room.say(send)
                    else :
                        await user_Info.contact.say(send) 
      #      if processes[result[1].state]['wait'] == 'true' :
      #          break
      #  else :
      #      break 


    if msg.text() == 'D': 
        contact = msg.talker()
        await msg.say('ding')
        
    if msg.text() == 'ding': 
        msg.talker = contact
        await contact.say('这是自动回复: dong dong dong')
        await msg.say('测试')
    if msg.text() == '图片':
        url = 'https://ai.bdstatic.com/file/403BC03612CC4AF1B05FB26A19D99BAF'
        # 构建一个FileBox
        #file_box_1 = FileBox.from_url(url=url, name='xx.jpg')
        '''
        with open('./image/3330.jpeg', 'rb') as f:
            content = base64.b64encode(f.read())
            file_box = FileBox.from_base64(name='3300177014.jpg', base64=content)
            await conversation.say(file_box)
        '''
        img_path = r'./images/3330.jpeg'
        file_box_3 = FileBox.from_file(img_path)
        #await msg.say('图片前')
        await msg.say(file_box_3)
        await msg.say('图片后')
  


async def on_scan(
        qrcode: str,
        status: ScanStatus,
        _data,
):
    print('Status: ' + str(status))
    print('View QR Code Online: https://wechaty.js.org/qrcode/' + qrcode)


async def on_login(user: Contact):
    print(user)


async def main():
    # 确保我们在环境变量中设置了WECHATY_PUPPET_SERVICE_TOKEN
    if 'WECHATY_PUPPET_SERVICE_TOKEN' not in os.environ:
        print('''
            Error: WECHATY_PUPPET_SERVICE_TOKEN is not found in the environment variables
            You need a TOKEN to run the Python Wechaty. Please goto our README for details
            https://github.com/wechaty/python-wechaty-getting-started/#wechaty_puppet_service_token
        ''')

    bot = Wechaty()

    bot.on('scan', on_scan)
    bot.on('login', on_login)
    bot.on('message', on_message)

    await bot.start()

    print('[Python Wechaty] Ding Dong Bot started.')


asyncio.run(main())