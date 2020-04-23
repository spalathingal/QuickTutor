from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image
from django.forms import ModelForm
from django import forms
from django.utils import timezone

import os

#seeing if travis work

TIMESLOT_OPTIONS = (
    ("1","5-15 minutes"),
    ("2","15-30 minutes"),
    ("3","30 minutes-1 hour"),
    ("4", "More than 1 hour"),
)

MEETING_PLACES = (
    ("Alderman Library","Alderman Library"),
    ("Clark (Brown) Library","Clark (Brown) Library"),
    ("Clemmons Library","Clemmons Library"),
    ("Starbucks (Corner)", "Starbucks (Corner)"),
    ("Starbucks (Newcomb)", "Starbucks (Newcomb)"),
    ("Argo Tea", "Argo Tea"),
    ("Einstein Bros (Rice)", "Einstein Bros (Rice)"),
    ("15|15", "15|15"),
)

#Create your models here

class AutoDateTimeField(models.DateTimeField):
    def pre_save(self, model_instance, add):
        return timezone.now()

class Message(models.Model):
    sender = models.ForeignKey(User, related_name="sender", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="receiver", on_delete=models.CASCADE)
    msg_content = models.TextField(verbose_name='message content', max_length=400, blank=True)
    created_at = models.TimeField(default=timezone.now)
    read = models.BooleanField(default=False)


class Fill_Out_Sheet(models.Model):
    has_tutor_accepted = models.BooleanField(default=False, null=True)
    has_tutor_rejected = models.BooleanField(default=False, null=True)
    no_response = models.BooleanField(default=True)
    sender = models.ForeignKey(User, related_name="Sender", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="Receiver", on_delete=models.CASCADE) 
    class_desc = models.CharField(max_length=30, blank=True)
    help_desc = models.TextField(max_length=100, blank=True)
    meeting_places = models.CharField(
        max_length = 200,
        choices = MEETING_PLACES,
        default = "15|15",
    )
    time_slot = models.CharField(
        max_length=20,
        choices = TIMESLOT_OPTIONS,
        default = '1'
        )
    def __str__(self):
        return self.class_desc

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True) 
    # location = models.CharField(max_length=30, blank=True)
    year = models.PositiveSmallIntegerField(blank=True, null=True)
    classes_taken = models.TextField(max_length=400, blank=True)
    # help_needed = models.TextField(max_length=300, blank=True)

    active_tutor = models.BooleanField(default=False)

    def __str__(self):
            return f'{self.user.username} Profile'

@receiver(models.signals.post_delete, sender=Profile)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding Profile object is deleted.
    """
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
