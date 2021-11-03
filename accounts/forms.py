from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model

class DateInput(forms.DateInput):
    input_type = 'date'

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'name', 'age', 'emp_id', 'emp_date', 'emp_grade', 'emp_team',)
        GRADE_CHOICES = (
            ('leader', 'leader'),   # 첫번째가 value
            ('follower', 'follower')
        )
        widgets = {
            'emp_date': DateInput(),
            'age' : DateInput(),
            'emp_grade' : forms.Select(choices=GRADE_CHOICES)
        }

class CustomUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm.Meta):
        model = get_user_model()
        fields = ('name', 'photo', 'emp_team',)
