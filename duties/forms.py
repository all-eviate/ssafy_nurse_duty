from django import forms
from .models import Nurse, Team

class NurseForm(forms.ModelForm):

    class Meta:
        model = Nurse
        fields = ('user', 'choices',)
        