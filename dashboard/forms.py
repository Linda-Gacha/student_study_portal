from dataclasses import fields
from logging import PlaceHolder
from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, User

class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ['title','description']

class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        fields =['subject', 'title', 'description', 'due', 'is_finished']
        widgets = {
        'due': forms.DateInput(
            format=('%d/%m/%Y %H:%M'),
            attrs={'class': 'form-control', 
               'placeholder': 'Select a date',
               'type': 'date'
              }),
        }

class DashboardForm(forms.Form):
    text = forms.CharField(max_length=100, label="Enter Your Search")

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title']


class ConversionForm(forms.Form):
    CHOICES = [('length','Length'),('mass','Mass')]
    measurement = forms.ChoiceField(choices= CHOICES, widget=forms.RadioSelect)

class ConversionLengthForm(forms.Form):
    CHOICES = [('yard','Yard'),('foot','Foot')]
    input = forms.CharField(required=False, label=False, widget=forms.TextInput(
        attrs= {'type':'number', 'placeholder': 'Enter The Number'}
    ))

    measure1 = forms.CharField(
        label='',widget=forms.Select(choices=CHOICES)
    )

    measure2 = forms.CharField(
        label='',widget=forms.Select(choices=CHOICES)
    )

class ConversionMassForm(forms.Form):
    CHOICES = [('pound','Pound'),('kilogram','Kilogram')]
    input = forms.CharField(required=False, label=False, widget=forms.TextInput(
        attrs= {'type':'number', 'placeholder': 'Enter The Number'}
    ))

    measure1 = forms.CharField(
        label='',widget=forms.Select(choices=CHOICES)
    )

    measure2 = forms.CharField(
        label='',widget=forms.Select(choices=CHOICES)
    )


class UserReg(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
