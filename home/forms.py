from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Profile
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime #for checking renewal date range.
    
class UserForm(ModelForm):
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)
    comfirm_password = forms.CharField(max_length=32, widget=forms.PasswordInput) 
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password2 = cleaned_data['comfirm_password']
        password1 = cleaned_data['password']

        if password1 != password2:
            raise ValidationError(_('password mismatched , enter same password in both field'))

        return cleaned_data

