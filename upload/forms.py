from django import forms
from .models import StatMaker

class StatMakerForm(forms.ModelForm):
    class Meta:
        model = StatMaker
        fields = ('file', )
