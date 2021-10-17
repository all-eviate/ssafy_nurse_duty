from django import forms
from .models import Nurse, Team

class SelectMonth(forms.ModelForm):
    MONTH_1 = 1
    MONTH_2 = 2
    MONTH_3 = 3
    MONTH_4 = 4
    MONTH_5 = 5
    MONTH_6 = 6
    MONTH_7 = 7
    MONTH_8 = 8
    MONTH_9 = 9
    MONTH_10 = 10
    MONTH_11 = 11
    MONTH_12 = 12
    MONTH_CHOiCES = [
        (MONTH_1, '1월'),
        (MONTH_2, '2월'),
        (MONTH_3, '3월'),
        (MONTH_4, '4월'),
        (MONTH_5, '5월'),
        (MONTH_6, '6월'),
        (MONTH_7, '7월'),
        (MONTH_8, '8월'),
        (MONTH_9, '9월'),
        (MONTH_10, '10월'),
        (MONTH_11, '11월'),
        (MONTH_12, '12월'),
    ]

    month = forms.ChoiceField(choices=MONTH_CHOiCES, widget=forms.Select)
    class Meta:
        model = Nurse
        fields = ('month',)

class NurseForm(forms.ModelForm):
    
    class Meta:
        model = Nurse
        fields = ('user', 'choices',)