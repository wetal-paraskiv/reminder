from django import forms
from . models import Reminder

from django.utils.timezone import datetime, timedelta
import pytz
local_tz = pytz.timezone('UTC')  # offset-aware datetime


class ReminderForm(forms.ModelForm):
    # you could override init method for specifying a certain css class for every field
    # def __init__(self, *args, **kwargs):
    #     super(ReminderForm, self).__init__(*args, **kwargs)
    #     self.fields['content'].widget.attrs.update(
    #         {'class': 'reminder-content'})

    class Meta:
        current_time = datetime.now().replace(tzinfo=pytz.utc).astimezone(local_tz)
        model = Reminder
        fields = ['text', 'date', 'repeat']
        # or using widgets to change attr class
        widgets = {
            'text': forms.TextInput(attrs={'class': 'reminder-content'}),
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'value': current_time}),
            # 'date': forms.TextInput(attrs={'type': 'datetime-local', 'value': current_time}),
        }


class EditReminderForm(forms.ModelForm):

    class Meta:
        current_time = datetime.now().replace(tzinfo=pytz.utc).astimezone(local_tz)
        model = Reminder
        fields = ['text', 'date', 'repeat', 'active']  # fields = '__all__'
        # or using widgets to change attr class
        widgets = {
            'text': forms.TextInput(attrs={'class': 'reminder-content'}),
            # 'date': forms.TextInput(attrs={'type': 'datetime-local'}),
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            # 'date': forms.DateTimeInput,
        }

    
