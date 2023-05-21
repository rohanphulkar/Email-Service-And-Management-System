from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Email
from accounts.models import User
from asgiref.sync import async_to_sync
import json
import markdown
from utils.check_spam_mail import check_spam_mail
from utils.username_suffix_check import check_suffix

class EmailConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "metabyte"

        # Add the consumer to the group
        await self.channel_layer.group_add(self.room_group_name,self.channel_name)

        # Accept the Websocket connection
        await self.accept()

        print("Email consumer connected successfully")
    
    async def disconnect(self, code):
        print("Email consumer disconnected with code: ", code)

        # Remove the consumer from the group
        await self.channel_layer.group_discard(self.room_group_name,self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        user = text_data_json['user']
        sender = text_data_json['sender']
        recipient = text_data_json['recipient']
        subject = text_data_json['subject']
        body = text_data_json['body']

        # Save the email item asynchronously
        email_obj = await self.save_email_item(user, sender, recipient, subject, body)

        # Send email to the group
        await self.channel_layer.group_send(self.room_group_name,{
            'type':'email_message',
            'user':user,
            'sender':str(email_obj.sender),
            'sender_name':str(email_obj.sender.name),
            'recipient':recipient,
            'subject':str(email_obj.subject),
            'body':email_obj.body,
            'id':str(email_obj.id),
            'spam':email_obj.spam,
            'timestamp':email_obj.timestamp.strftime('%b %d, %Y, %H:%M %p')
        })
    
    async def email_message(self,event):
        id = event['id']
        user = event['user']
        sender = event['sender']
        sender_name = event['sender_name']
        recipient = event['recipient']
        subject = event['subject']
        body = event['body']
        spam = event['spam']
        timestamp = event['timestamp']


        # Send the email message to the consumer
        await self.send(text_data=json.dumps({
            'type':'email',
            'id':id,
            'user':user,
            'sender':sender,
            'sender_name':sender_name,
            'recipient':recipient,
            'subject':subject,
            'body':body,
            'spam':spam,
            'timestamp':timestamp
        }))
    
    @database_sync_to_async
    def create_email_item(self,user,sender,recipient,subject,body):
        user = User.objects.get(id=user)
        sender = User.objects.get(id=sender)
        body = markdown.markdown(body)
        obj = Email.objects.create(user=user, sender=sender, subject=subject, body=body)
        for recipient in recipient:
            recipient = check_suffix(recipient)
            recipient = User.objects.get(username=recipient)
            obj.recipients.add(recipient)
        spam = check_spam_mail(subject) or check_spam_mail(body)
        if spam:
            obj.spam = True
        obj.save()
        return obj
    
    async def save_email_item(self,user,sender,recipient,subject,body):
        return await self.create_email_item(user,sender,recipient,subject,body)
    