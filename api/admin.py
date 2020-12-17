from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import NoticeBoard, Event, MessageUser, UserCategory, CustomUser, StuffUser, ClubFacility, \
    ClubFacilityDetail
from .forms import CustomUserCreationForm, CustomUserChangeForm
from import_export.admin import ImportExportModelAdmin


# Register your models here.

class CustomUserAdmin(UserAdmin, ImportExportModelAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': (
            'email',
            "image_medium",
            "image_thumbnail",
            'password',
            'phone_primary',
            'phone_secondary',
            'club_ac_number',
            'category_name',
            'designation',
            'membership_date',
            'birthday',
            'marital_status',
            'marriage_anniversary',
            'spouse',
            'father_name',
            'mother_name',
            'address',
            'nationality',
            'blood_group',
            'religion',
            'gender',
            'profession',
            'education',
            'status'
        )}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'username',
                'first_name',
                'last_name',
                "image_medium",
                "image_thumbnail",
                'password1',
                'password2',
                'is_staff',
                'is_active',
                'phone_primary',
                'phone_secondary',
                'club_ac_number',
                'category_name',
                'designation',
                'membership_date',
                'birthday',
                'marital_status',
                'marriage_anniversary',
                'spouse',
                'father_name',
                'mother_name',
                'address',
                'nationality',
                'blood_group',
                'religion',
                'gender',
                'profession',
                'education',

            )
        }
         ),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(StuffUser, ImportExportModelAdmin)


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


@admin.register(ClubFacility)
class ClubFacilityAdmin(admin.ModelAdmin):
    pass


@admin.register(ClubFacilityDetail)
class ClubFacilityDetailAdmin(admin.ModelAdmin):
    pass
