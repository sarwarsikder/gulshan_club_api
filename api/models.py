from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, AbstractUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager

from django.contrib.auth import get_user_model
# Create your models here.

class UserCategory(models.Model):
    category_name = models.CharField(max_length=200)
    description = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)
    deleted_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.category_name

    class Meta:
        ordering = ['category_name', 'description', 'created_at', 'deleted_at']




class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)

    material_types = (
        ("Married", "Married"),
        ("Unmarried", "Unmarried"),
        ("Divorce", "Divorce"),
    )
    gender_types = (
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other"),
    )
    phone_primary = models.CharField(max_length=200, null=True)
    phone_secondary = models.CharField(max_length=200, null=True)
    club_ac_number = models.CharField(max_length=200)
    club_ac_number = models.CharField(max_length=200)
    category_name = models.ForeignKey(UserCategory, on_delete=models.DO_NOTHING,null=True)
    membership_date = models.DateField(null=True)
    birthday = models.DateField(null=True)
    material_status = models.CharField(choices=material_types, max_length=50, null=True)
    marriage_anniversary = models.DateField(null=True)
    spouse = models.CharField(max_length=200, null=True)
    father_name = models.CharField(max_length=200, null=True)
    mother_name = models.CharField(max_length=200, null=True)
    address = models.TextField(null=True)
    nationality = models.CharField(max_length=50, null=True)
    blood_group = models.CharField(max_length=10, null=True)
    religion = models.CharField(max_length=25, null=True)
    gender = models.CharField(choices=gender_types, max_length=50, null=True)
    profession = models.CharField(max_length=200, null=True)
    education = models.TextField(null=True)
    opt = models.CharField(max_length=10, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)
    deleted_at = models.DateTimeField(auto_now_add=True, null=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    def __str__(self):
        return self.username


User = get_user_model()


class StuffUser(models.Model):
      stuff_name = models.CharField(max_length= 200)
      image = models.ImageField(blank=True, null=True)
      designation_group = models.CharField(max_length= 300)
      designation = models.CharField(max_length= 300)
      mobile_number_primary = models.CharField(max_length= 300)
      mobile_number_secondary = models.CharField(max_length= 300, null=True, blank=True)
      created_at = models.DateTimeField(null=True, blank=True)

      def __str__(self):
          return self.stuff_name

      class Meta:
          ordering = ['stuff_name', 'designation_group', 'designation', 'mobile_number_primary']

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
    tag = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)
    deleted_at = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['title', 'message', 'tag', 'created_at', 'updated_at']


class Event(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(unique=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    url = models.URLField(blank=True)
    description = models.TextField()
    image = models.ImageField(blank=True, null=True)
    image_alt_text = models.CharField(max_length=250, null=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=True)
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['start_date', 'end_date', 'name', 'slug', 'created']

class ClubFacility(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    image = models.ImageField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True, editable=True)
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name', 'description', 'image']
class ClubFacilityDetail(models.Model):
    name = models.CharField(max_length=250)
    club_facility = models.ForeignKey(ClubFacility, on_delete=models.DO_NOTHING)
    description = models.TextField()
    image = models.ImageField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True, editable=True)
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name', 'description', 'image']
