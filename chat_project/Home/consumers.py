#routing se phle ye kiye
#for async we just need to write sync
#ye wala page same as views
#isme jo daata hai vo dono me jaa skta
from channels.consumer import SyncConsumer,AsyncConsumer
from channels.exceptions import StopConsumer
import asyncio
import json
from time import sleep
from asgiref.sync import async_to_sync #this convert async to sync

class MySyncConsumer(SyncConsumer):
    

    def websocket_connect(self,event):
        print('connected')
        print('channel layer is ', self.channel_name)
        self.send({
            'type':'websocket.accept'
        })

    def websocket_receive(self , event):
        print('received',event )
        print(event['text'])
        #adding channel to new or existing group
        async_to_sync(self.channel_layer.group_add)('friend',self.channel_name)
        self.send({ # server ko jo data bhejna hai
            'type':'websocket.send',
            'text':'hi' #error maine dobara string me change kr diya tha
        })
        # real time data
        # for i in range(10):
        #     self.send({ # mssg sent to server jo console me dikhga of webbrowser
        #         'type':'websocket.send',
        #         'text':str(i)
        #     })#this will create on time numbers
        #     sleep(1)
        async_to_sync(self.channel_layer.group_send)('friend',{
            'type':'chat.message',
            'msg':event['text']
        })
        
    def chat_message(self,event):#group me mssg bhejne ke baad isme data jaega
        print('event...',event["msg"])
        self.send({
            'type':'websocket.send',
            'text':event["msg"]
        }) #on message me jaega
        # print('actual data',event['msg'])
        # data jo hai vo server me jata hai vha se hm query selector use krke done me message bej de rhe hai
 


    def websocket_disconnect(self,event):
        print('disconnect')
        #now discard the channel name vid - 
        self.channel_layer.group_discard('friend',self.channel_name)
        print('channel discarded')
        raise StopConsumer()
    
class MyAsyncConsumer(AsyncConsumer):
    

    async def websocket_connect(self,event):
        print('connected')
        print('channel layer is ', self.channel_name)
        await self.send({
            'type':'websocket.accept'
        })

    async def websocket_receive(self , event):
        print('received',event )
        print(event['text'])
        #adding channel to new or existing group
        self.channel_layer.group_add('friend',self.channel_name)
        self.send({ # server ko jo data bhejna hai
            'type':'websocket.send',
            'text':'hi' #error maine dobara string me change kr diya tha
        })
        # real time data
        # for i in range(10):
        #     self.send({ # mssg sent to server jo console me dikhga of webbrowser
        #         'type':'websocket.send',
        #         'text':str(i)
        #     })#this will create on time numbers
        #     sleep(1)
        self.channel_layer.group_send('friend',{
            'type':'chat.message',
            'msg':event['text']
        })
        
    async def chat_message(self,event):#group me mssg bhejne ke baad isme data jaega
        print('event...',event["msg"])
        await self.send({
            'type':'websocket.send',
            'text':event["msg"]
        }) #on message me jaega
        # print('actual data',event['msg'])
        # data jo hai vo server me jata hai vha se hm query selector use krke done me message bej de rhe hai
 


    async def websocket_disconnect(self,event):
        print('disconnect')
        #now discard the channel name vid - 
        await self.channel_layer.group_discard('friend',self.channel_name)
        print('channel discarded')
        raise StopConsumer()

# when writing consumer we use as_asgi() -- same as view
# class MyAsyncConsumer(AsyncConsumer):
#     async def websocket_connect(self,event):
#         print('connected')
#         await self.send({  #data ko accept bhi to krna hai
#             'type':'websocket.accept',
#         })

#     async def websocket_receive(self , event):
#         print('received',event)
#         print(event['text'])
#         # real time data
#         for i in range(10):
#             await self.send({ # mssg sent to client ----- error if we didnt write await
#                 'type':'websocket.send',
#                 'text':str(i)
#             })#this will create on time numbers
#             await asyncio.sleep(1)

#     async def websocket_disconnect(self,event):
#         print('disconnect')
#         raise StopConsumer()
        # ws://127.0.0.1:8000/ws/sc 


# note data jo aata hai vo ek dictionary k fomr me aata so event['text'] krke hm use access kr skte
#sync me ek k sath messages deliver nhi ho jata tb tk dusre me mssg start nhi hoga

"""
in js file websocket bnane k liye 
var ws = new WebSocket('link ws wali')
1.onopen function tells whether connection ready to send data
    ws.onopen = function(event){
    clog - event
2.onmessage - jb server me client data bhejta hai
    ws.onmessage = function(event){
    clog - event
2.onerror - when error
    ws.error = function(event){
    clog - event
4.ws.onclose = function(event)

5.channel layer is used to communicate between different consumers
6.channels are first in first out
7.channels me name pta hona jrurui hai
8.multiple channel are grouped to make a broadcast
9.messages must be a dict
10channel layer provide us
    get_channel_layer() - this func is used to get default channel layer

"""