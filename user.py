
from wechaty import (
    Contact,
    Room,
)

class User(object):
    def __init__(self, contactid):
        self.contactid = contactid
 
    #getter
    @property
    def room(self):
        return self.__room
 
    #settter
    @room.setter
    def room(self, room : Room):
        self.__room = room
        
    #getter
    @property
    def contact(self):
        return self.__contact
 
    #settter
    @contact.setter
    def contact(self, contact : Contact):
        self.__contact = contact
        
    #getter
    @property
    def roomtopic(self):
        return self.__roomtopic
 
    #settter
    @roomtopic.setter
    def roomtopic(self, roomtopic):
        self.__roomtopic = roomtopic
        
    #getter
    @property
    def contactid(self):
        return self.__contactid
 
    #settter
    @contactid.setter
    def contactid(self, contactid):
        self.__contactid = contactid

    #getter
    @property
    def chlvl(self):
        return self.__chlvl
 
    #settter
    @chlvl.setter
    def chlvl(self, chlvl):
        self.__chlvl = chlvl
    
    #getter
    @property
    def bkstck(self):
        return self.__bkstck
 
    #settter
    @bkstck.setter
    def bkstck(self, bkstck):
        self.__bkstck = bkstck

    #getter
    @property
    def state(self):
        return self.__state
 
    #settter
    @state.setter
    def state(self, state):
        self.__state = state

    #getter
    @property
    def qstntype(self):
        return self.__qstntype
 
    #settter
    @qstntype.setter
    def qstntype(self, qstntype):
        self.__qstntype = qstntype

    #getter
    @property
    def chose(self):
        return self.__chose
 
    #settter
    @qstntype.setter
    def chose(self, chose):
        self.__chose = chose

    #getter
    @property
    def model(self):
        return self.__model
 
    #settter
    @model.setter
    def model(self, model):
        self.__model = model

    #getter
    @property
    def imgpath(self):
        return self.__imgpath
 
    #settter
    @imgpath.setter
    def imgpath(self, imgpath):
        self.__imgpath = imgpath

    #getter
    @property
    def cls(self):
        return self.__cls
 
    #settter
    @cls.setter
    def cls(self, cls):
        self.__cls = cls
