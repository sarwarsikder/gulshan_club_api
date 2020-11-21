from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import NoticeBoard, Event, MessageUser, UserCategory, CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm
from import_export.admin import ImportExportModelAdmin

# Register your models here.

class CustomUserAdmin(UserAdmin,ImportExportModelAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)


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

