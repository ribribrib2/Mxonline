from django import forms
from operation.models import UserAsk

class UserAskForms(forms.ModelForm):
    class Meta:
        model = UserAsk
        fields = ['name','mobile','course_name']
