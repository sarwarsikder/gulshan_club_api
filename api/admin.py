from django.contrib import admin
from .models import User, NoticeBoard, Event, MessageUser, UserCategory

# Register your models here.

@admin.register(NoticeBoard)
class NoticeBoardAdmin(admin.ModelAdmin):
    pass

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass

@admin.register(MessageUser)
class MessageUserAdmin(admin.ModelAdmin):
    pass

@admin.register(UserCategory)
class UserCategoryAdmin(admin.ModelAdmin):
    pass

