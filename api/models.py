from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from stdimage import StdImageField

from .managers import CustomUserManager


# Create your models here.


def image_variations():
    return {
        'large': (600, 400),
        'thumbnail': (100, 100, True),
        'medium': (300, 200)
    }


def image_storage(fil_path):
    location = u'{0}/'.format(fil_path)
    return location


def image_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/my_sell/picture/<filename>
    return u'picture/{0}'.format(filename)


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
    email = models.EmailField(_('email address'))

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

    user_status = (
        ("doard_director", "Board Of Director"),
        ("active", "Active"),
        ("inactive", "Inactive"),
    )

    image_medium = StdImageField(upload_to=image_storage('member_user/medium'), variations={
        'medium': (300, 200)
    }, blank=True, null=True)
    image_thumbnail = StdImageField(upload_to=image_storage('member_user/thumbnail'), variations={
        'thumbnail': (100, 100, True),
    }, blank=True, null=True)
    phone_primary = models.CharField(max_length=200, null=True, blank=True)
    phone_secondary = models.CharField(max_length=200, null=True, blank=True)
    club_ac_number = models.CharField(max_length=200, blank=True)
    category_name = models.ForeignKey(UserCategory, on_delete=models.DO_NOTHING, null=True, blank=True)
    designation = models.CharField(max_length=250, null=True, blank=True)
    membership_date = models.DateField(null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    marital_status = models.CharField(choices=material_types, max_length=50, null=True, blank=True)
    marriage_anniversary = models.DateField(null=True, blank=True)
    spouse = models.CharField(max_length=200, null=True, blank=True)
    father_name = models.CharField(max_length=200, null=True, blank=True)
    mother_name = models.CharField(max_length=200, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    nationality = models.CharField(max_length=50, null=True, blank=True)
    blood_group = models.CharField(max_length=10, null=True, blank=True)
    religion = models.CharField(max_length=25, null=True, blank=True)
    gender = models.CharField(choices=gender_types, max_length=50, null=True, blank=True)
    profession = models.CharField(max_length=200, null=True, blank=True)
    education = models.TextField(null=True, blank=True)
    opt = models.CharField(max_length=10, null=True, blank=True)
    opt_time = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    status = models.CharField(choices=user_status, max_length=50, null=True, blank=True, default='Active')
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    deleted_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    def __str__(self):
        return self.username


User = get_user_model()


class StuffUser(models.Model):
    stuff_name = models.CharField(max_length=200)
    image_medium = StdImageField(upload_to=image_storage('stuff_user/medium'), variations={
        'medium': (300, 200)
    }, blank=True, null=True)
    image_thumbnail = StdImageField(upload_to=image_storage('stuff_user/thumbnail'), variations={
        'thumbnail': (100, 100, True),
    }, blank=True, null=True)
    designation_group = models.CharField(max_length=300)
    designation = models.CharField(max_length=300)
    mobile_number_primary = models.CharField(max_length=300)
    mobile_number_secondary = models.CharField(max_length=300, null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.stuff_name

    class Meta:
        ordering = ['stuff_name', 'designation_group', 'designation', 'mobile_number_primary']


class MessageManager(models.Manager):

    def inbox_for(self, user):
        """
        Returns all messages that were received by the given user and are not
        marked as deleted.
        """
        sql = self.filter(
            Q(recipient=user) | Q(sender=user),
            recipient_deleted_at__isnull=True,
            parent_msg=None
        )
        print(sql.query)
        return sql
    def count_unread_message(self, user, recipient, max_limit=5):
        """
        Returns all messages that were received by the given user and are not
        marked as deleted.
        """
        sql = self.filter(
            Q(recipient=user) & Q(sender=recipient) | Q(recipient=recipient) & Q(sender=user),
            read_at=None,
            recipient_deleted_at__isnull=True)[:max_limit]
        return len(sql)

    def get_last_message(self, user, recipient, max_limit=5):
        """
        Returns all messages that were received by the given user and are not
        marked as deleted.
        """
        sql = self.filter(
            Q(recipient=user) & Q(sender=recipient) | Q(recipient=recipient) & Q(sender=user),
            recipient_deleted_at__isnull=True)[:max_limit]
        print(sql.query)
        return sql

    def parent_for(self, user, recipient):
        """
        Returns all messages that were received by the given user and are not
        marked as deleted.
        """
        return self.filter(
            Q(recipient=user) & Q(sender=recipient) | Q(recipient=recipient) & Q(sender=user),
            recipient_deleted_at__isnull=True,
            parent_msg=None
        )

    def inbox_for_single_user(self, user, parent_id):
        """
        Returns all messages that were received by the given user and are not
        marked as deleted.
        """
        return self.filter(
            Q(parent_msg=parent_id) | Q(id=parent_id),
            recipient_deleted_at__isnull=True
        )

    def select_for_single_user(self, user, recipient):
        """
        Returns all messages that were received by the given user and are not
        marked as deleted.
        """
        return self.filter(
            Q(recipient=user) & Q(sender=recipient) | Q(recipient=recipient) & Q(sender=user),
            recipient_deleted_at__isnull=True,
        )

    def outbox_for(self, user):
        """
        Returns all messages that were sent by the given user and are not
        marked as deleted.
        """
        return self.filter(
            sender=user,
            sender_deleted_at__isnull=True,
        )

    def trash_for(self, user):
        """
        Returns all messages that were either received or sent by the given
        user and are marked as deleted.
        """
        return self.filter(
            recipient=user,
            recipient_deleted_at__isnull=False,
        ) | self.filter(
            sender=user,
            sender_deleted_at__isnull=False,
        )


class MessageUser(models.Model):
    subject = models.TextField(max_length=2000)
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_messages', null=True, blank=True,
                                  on_delete=models.CASCADE)
    parent_msg = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    sent_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    read_at = models.DateTimeField(null=True, blank=True)
    replied_at = models.DateTimeField(null=True, blank=True)
    sender_deleted_at = models.DateTimeField(null=True, blank=True)
    recipient_deleted_at = models.DateTimeField(null=True, blank=True)

    objects = MessageManager()

    def new(self):
        """returns whether the recipient has read the message or not"""
        if self.read_at is not None:
            return False
        return True

    def replied(self):
        """returns whether the recipient has written a reply to this message"""
        if self.replied_at is not None:
            return True
        return False

    def __str__(self):
        return self.subject

    class Meta:
        ordering = ['-sent_at']
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")


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
    image_medium = StdImageField(upload_to=image_storage('event/medium'), variations={
        'medium': (300, 200)
    }, blank=True, null=True)
    image_thumbnail = StdImageField(upload_to=image_storage('event/thumbnail'), variations={
        'thumbnail': (100, 100, True),
    }, blank=True, null=True)
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
    image_medium = StdImageField(upload_to=image_storage('club_facility/medium'), variations={
        'medium': (300, 200)
    }, blank=True, null=True)
    image_thumbnail = StdImageField(upload_to=image_storage('club_facility/thumbnail'), variations={
        'thumbnail': (100, 100, True),
    }, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True, editable=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name', 'description']


class ClubFacilityDetail(models.Model):
    name = models.CharField(max_length=250)
    club_facility = models.ForeignKey(ClubFacility, on_delete=models.DO_NOTHING)
    description = models.TextField()
    image_medium = StdImageField(upload_to=image_storage('club_facility_detail/medium'), variations={
        'medium': (300, 200)
    }, blank=True, null=True)
    image_thumbnail = StdImageField(upload_to=image_storage('club_facility_detail/thumbnail'), variations={
        'thumbnail': (100, 100, True),
    }, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True, editable=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name', 'description', 'image_medium', 'image_thumbnail']
