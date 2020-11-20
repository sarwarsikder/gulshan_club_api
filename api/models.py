from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class MessageUser(models.Model):
    subject = models.TextField(max_length=2000)
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.PROTECT)
    recipient = models.ForeignKey(User, related_name='received_messages', null=True, blank=True, on_delete=models.SET_NULL)
    parent_msg = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(null=True, blank=True)
    read_at = models.DateTimeField(null=True, blank=True)
    replied_at = models.DateTimeField(null=True, blank=True)
    sender_deleted_at = models.DateTimeField(null=True, blank=True)
    recipient_deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.subject
    
    class Meta:
        ordering = ['subject', 'sender', 'recipient', 'created_at']



class NoticeBoard(models.Model):
    title = models.CharField(max_length=100)
    message = models.TextField(max_length=2000)
    tag = models.CharField(max_length=50, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)
    deleted_at = models.DateTimeField(auto_now_add=False, null=True)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['title', 'message', 'created_at', 'updated_at']


class Event(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(unique=True)
    start_date = models.DateField()
    end_date = models.DateField()
    url = models.URLField(blank=True)
    description = models.TextField()
    image = models.ImageField(blank=True)
    image_alt_text = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['start_date', 'end_date', 'name']