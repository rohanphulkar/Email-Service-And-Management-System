from django.db import models
import uuid
from accounts.models import User
from ckeditor.fields import RichTextField

class Email(models.Model):
    id = models.UUIDField(default=uuid.uuid4,primary_key=True,editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='email_user')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='email_sender')
    recipients = models.ManyToManyField(User,related_name="email_recipients")
    subject = models.CharField(max_length=255)
    body = RichTextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    archived = models.BooleanField(default=False)
    starred = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    spam = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    
    class Meta:
        ordering = ['-timestamp']

    def get_recipient(self):
        return ",".join([str(recipient) for recipient in self.recipients.all()])