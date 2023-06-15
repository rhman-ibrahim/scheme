from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
from .models import Room, Message
from user.models import Account
import json


class ChatConsumer(AsyncWebsocketConsumer):

    @sync_to_async
    def is_member(self, user, room):
        if  room.circle.user_role(user) != None:
            return True
        return False

    @database_sync_to_async
    def get_room(self, serial):
        return Room.objects.get(space=serial)
    
    @database_sync_to_async
    def get_user(self, username):
        return Account.objects.get(username=username)
    
    @database_sync_to_async
    def load_messages(self, room):
        return [
            json.dumps
            (
                {
                    'sender': message.sender.username,
                    'body': message.body,
                }
            )
            for message in Message.objects.filter(room=room)[:100]
        ]

    @database_sync_to_async
    def save(self, room, user, body):
        message = Message.objects.create(room=room, sender=user, body=body)
        message.save()

    async def connect(self):

        self.user       = self.scope["user"]                                                # get the user object (scope).
        self.room       = await self.get_room(self.scope['url_route']['kwargs']['serial'])  # get room id (scope) to get the room object.
        self.member     = await self.is_member(self.user, self.room)                        # check if user is a member of the room.
        self.username   = self.user.username                                                # extract username from user object.
        self.group_name = self.room.space                                                    # create a name for the group.

        if not self.room or not self.member:
            await self.close()                                                              # close connection if the user is not a memmber.
        else:
            await self.channel_layer.group_add(                                             # add the new connected channel to the group.
                self.group_name,                                                            # the group  name.
                self.channel_name                                                           # the self assigned channel name.
            )
            await self.accept()                                                             # accept the connection.
            await self.channel_layer.group_send(                                            # background worker.
                self.group_name,
                {
                    'type': 'load',                                                         # the handler.
                    'load': await self.load_messages(self.room)                             # sending the room object to get the messages.
                }
            )
            await self.channel_layer.group_send(                                            # background worker.
                self.group_name,
                {
                    'type': 'notify',                                                       # the handler.
                    'user': f'{self.username} has joined the room',                         # the 'notification' data.
                },
            )

    async def receive(self, text_data):
        data = json.loads(text_data)                                                        # load the data sent by the client.
        user = await self.get_user(data['username'])                                        # get the user's object of the sender client.
        await self.save(self.room, user, data['message'])                                   # save the message object to the database.
        await self.channel_layer.group_send(                                                # background worker
            self.group_name,
            {
                'type':'message',                                                           # the handler.
                'username':data['username'],
                'message':data['message'],
            }
        )

    async def disconnect(self, code):
        await self.channel_layer.group_send(                                                # background worker.
            self.group_name,
            {
                'type': 'notify',                                                           # the handler.
                'user': f'{self.username} has left the room',
            }
        )
        await self.channel_layer.group_discard(                                             # removing the connected channel from the group.
            self.group_name,
            self.channel_name
        )

    # defining the background worker handler.
    async def notify(self, event):
        await self.send(
            text_data = json.dumps(
                {
                    'event': 'notify',
                    'user': event['user']
                }
            )
        )
        
    # defining the background worker handler.
    async def load(self, event):
        await self.send(                                            
            text_data=json.dumps(
                {
                    'event': 'load',
                    'messages': event['load']
                }
            )
        )
        
    # defining the background worker handler.
    async def message(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    'event': 'message',
                    'body': event['message'],
                    'sender': event['username']
                }
            )
        )