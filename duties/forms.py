from django import forms
from .models import Nurse

class NurseForm(forms.ModelForm):

    class Meta:
        model = Nurse
        fields = '__all__'
        