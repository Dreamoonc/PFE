# from channels.generic.websocket import WebsocketConsumer,AsyncWebsocketConsumer
# from channels.db import database_sync_to_async
# from asgiref.sync import async_to_sync,sync_to_async
# from channels.layers import get_channel_layer
# from .models import *


# @database_sync_to_async
# def get_user(user_id):
#     try:
#         return User.objects.get(id=user_id)
#     except:
#         return "user doesn't exist"

# @database_sync_to_async
# def create_notification(receiver,typeof="task_created",status="unread"):
#     notification_to_create=Notification.objects.create(user_revoker=receiver,type_of_notification=typeof)
#     print('I am here to help')
#     return (notification_to_create.user_revoker.username,notification_to_create.type_of_notification)


# class NotificationConsumer(AsyncWebsocketConsumer):
#     async def websocket_connect(self,event):
#         print(self.scope)
#         await self.accept()
#         await self.send(json.dumps({
#             "type":"websocket.send",
#             "text":"hello world"
#         })) 
#         self.room_name='test_consumer'   
#         self.room_group_name='test_consumer_group'
#         await self.channel_layer.group_add(self.room_group_name,self.channel_name)
#         self.send({
#             "type":"websocket.send",
#             "text":"room made"
#         })

#     async def websocket_receive(self,event):
#         print(event)
#         data_to_get=json.loads(event['text'])
#         user_to_get=await get_user(int(data_to_get))
#         print(user_to_get)
#         get_of=await create_notification(user_to_get)
#         self.room_group_name='test_consumer_group'
#         channel_layer=get_channel_layer()
#         await (channel_layer.group_send)(
#             self.room_group_name,
#             {
#                 "type":"send_notification",
#                 "value":json.dumps(get_of)
#             }
#         )
#         print('receive',event)

#     async def websocket_disconnect(self,event):
#         print('disconnect',event)

#     async def send_notification(self,event):
#         await self.send(json.dumps({
#             "type":"websocket.send",
#             "data":event
#         }))
#         print('I am here')
#         print(event)

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.auth import login

class TestConsumer(WebsocketConsumer):
    
    def connect(self):
        self.room_name = "test_consumer"
        self.room_group_name = "test_consumer_group"
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
        self.user = self.scope["user"]
        print(vars(self.user))
        print(vars(self))
        self.send(text_data=json.dumps({'status' : 'connected from django channels'}))
        
    
    
    def receive(self, text_data):
        print(text_data)
        self.send(text_data=json.dumps({'status' : 'we got you'}))


    def disconnect(self , *args, **kwargs):
        print('disconnected')
    
    
    def send_notification(self , event):
        print('send notification')
        data = json.loads(event.get('value'))
        self.send(text_data=json.dumps({'payload' : data}))
        print('send notification')



# class NewConsumer(AsyncJsonWebsocketConsumer):
    
#     async def connect(self):
#         self.room_name = 'new_consumer'
#         self.room_group_name = "new_consumer_group"
        
#         await(self.channel_layer.group_add)(
#             self.room_group_name,
#             self.channel_name
#         )
        
#         await self.accept()
#         self.user = self.scope["user"]
#         print(self.user)
#         await self.send(text_data=json.dumps({'status' : 'connected from new async json consumer'}))
        
        
#     async def receive(self, text_data):
#         print(text_data)
#         await self.send(text_data=json.dumps({'status' : 'we got you'}))


#     async def disconnect(self , *args, **kwargs):
#         await print('disconnected')
    
#     async  def send_notification(self , event):
#         data = json.loads(event.get('value'))
#         await self.send(text_data=json.dumps({'payload' : data}))