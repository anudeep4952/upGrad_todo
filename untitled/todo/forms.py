from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from todo.models import Document
from datetime import datetime
from bootstrap_datepicker_plus import DatePickerInput
from django.contrib.admin import widgets

class user_SignUpForm(UserCreationForm):

    first_name = forms.CharField(max_length=30, required=True, help_text='*required')
    last_name = forms.CharField(max_length=30, required=True, help_text='*required')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name','email','password1', 'password2', )


class DocumentForm(forms.ModelForm):
      date = forms.DateField(widget=forms.SelectDateWidget,initial=datetime.today())
      time=forms.TimeField(widget=forms.TimeInput(format='%H:%M'))
      class Meta:
            model = Document
            fields=('task','date','time')


