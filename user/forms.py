from django.shortcuts import redirect, HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth.models import User
from user.models import Profile, Message
from django import forms
from user.models import Fill_Out_Sheet

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

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('active_tutor', 'bio', 'year', 'classes_taken')
        labels = {
            "year":"Graduation year",
        }

class MessageForm(forms.ModelForm):
    recipient = forms.EmailField(label="Recipient's email", max_length=200)
    class Meta:
        model = Message
        fields = ('recipient', 'msg_content')
        labels = {
            "recipient":"",
            "msg_content":"",
        }

class ChatForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('msg_content',)

        
class FillOutSheetForm(forms.ModelForm):
    meeting_places = forms.MultipleChoiceField(
        required=True,
        widget = forms.CheckboxSelectMultiple,
        choices = MEETING_PLACES,
    )
    class Meta:
        model = Fill_Out_Sheet
        fields = ('class_desc','help_desc','time_slot','meeting_places')
        labels = {
            "class_desc":"",
            "help_desc":"",
            "time_slot":"",
            "meeting_places":"",
        }

class ActiveTutorForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('active_tutor',)
