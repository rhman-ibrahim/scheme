from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
from .models import Room, Message
from user.models import Account
import json


class ChatConsumer(AsyncWebsocketConsumer):

    @sync_to_async
    def is_member(self, user, room):
        if  room.circle.user_role(user) != None: return True
        return False

    @database_sync_to_async
    def get_room(self, serial):
        return Room.objects.get(space=serial)
    
    @database_sync_to_async
    def get_user(self, username):
        return Account.objects.get(username=username)
    
    @database_sync_to_async
    def load_messages(self, room):
        # Convert the messages from Python dicts to JSON objects.
        return [
            json.dumps
            (
                {
                    'body': message_DICT_data.body,
                    'sender': message_DICT_data.sender.username
                }
            )
            for message_DICT_data in Message.objects.filter(room=room)[:100]
        ]

    @database_sync_to_async
    def save(self, room, user, body):
        message = Message.objects.create(room=room, sender=user, body=body)
        message.save()

    async def connect(self):

        self.user       = self.scope["user"]                                                # Get the user object (scope),
        self.room       = await self.get_room(self.scope['url_route']['kwargs']['serial'])  # get room id (scope) to get the room object,
        self.member     = await self.is_member(self.user, self.room)                        # check if user is a member of the room,
        self.username   = self.user.username                                                # extract username from user object,
        self.group_name = self.room.space                                                   # set the group name.

        if not self.room or not self.member:

            # Close connection if the user is not a memmber.
            await self.close()

        else:
            
            # Accept the connection.
            await self.accept()
            
            # Add the new connected channel to the group.
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            
            # Directly after accepting the connection.

            # 1 - Send the 'messages' data to the channels' group,
            # through the 'load' background worker.
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'load',
                    'messages': await self.load_messages(self.room)
                }
            )
            
            # 2 - Send the 'notification' data to the channels' group.
            # through the 'notify' background worker.
            await self.channel_layer.group_send(
                self.group_name,
                {
                    
                    'type': 'notify',
                    'notification': f'{self.username} has joined the room',
                },
            )

    async def receive(self, text_data):

        # Parse the receivied JSON data.
        sever_DICT_data = json.loads(text_data)
        
        # Save the message to the database.
        await self.save(
            self.room,
            await self.get_user(sever_DICT_data['sender']),
            sever_DICT_data['body']
        )
        
        # Send the 'message' data to the channels' group.
        # through the 'message' background worker.
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type':'message',
                'body':sever_DICT_data['body'],
                'sender':sever_DICT_data['sender']
            }
        )

    async def disconnect(self, code):
        
        # Send the 'notification' data to the channels' group.
        # through the 'notify' background worker.
        await self.channel_layer.group_send(                                                
            self.group_name, 
            {
                'type': 'notify', 
                'notification': f'{self.username} has left the room',
            }
        )

        # Removing the connected channel from the group.
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )


    # The background workers, convreting the data sent by the server
    # to JSON objects & sending it to the each client channel in real-time.

    # 'notification' 
    async def notify(self, server_DICT_data):
        await self.send(
            text_data = json.dumps(
                {
                    'event': 'notify',
                    'notification': server_DICT_data['notification']
                }
            )
        )
    
    # 'messages'
    async def load(self, server_DICT_data):
        await self.send(                                            
            text_data = json.dumps(
                {
                    'event': 'load',
                    'messages': server_DICT_data['messages']
                }
            )
        )
    
    # 'message'
    async def message(self, server_DICT_data):
        await self.send(
            text_data = json.dumps(
                {
                    'event': 'message',
                    'body': server_DICT_data['body'],
                    'sender': server_DICT_data['sender']
                }
            )
        )