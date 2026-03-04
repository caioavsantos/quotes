from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.core import validators
from .models import Quote, Thinker

class QuoteForm(ModelForm):
    class Meta:
        model = Quote
        fields = ["thinker", "quote", "reference", "explanation"]

        #add widgets and fix html file

class ThinkerForm(ModelForm):
    class Meta:
        model = Thinker
        fields = ["name", "picture"]