# forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Movie, UserRanking
from django.contrib.auth.models import User
from django.shortcuts import render, redirect


class RegistrationForm(UserCreationForm):
    email = forms.EmailField()
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

class AddToRankingForm(forms.Form):
    position = forms.IntegerField()
    title = forms.CharField(max_length=255)
    overview = forms.CharField(widget=forms.Textarea)
    poster_path = forms.CharField(max_length=255)