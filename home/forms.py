from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Profile,Course,Lesson,Post
from django.core.exceptions import ValidationError
from django_countries.widgets import CountrySelectWidget
from django.utils.translation import ugettext_lazy as _
import datetime #for checking renewal date range.
    
class UserForm(ModelForm):
    password = forms.CharField(max_length=32, widget=forms.PasswordInput(attrs={'class' : 'form-control'}))
    comfirm_password = forms.CharField(max_length=32, widget=forms.PasswordInput(attrs={'class' : 'form-control'})) 

    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']
        widgets = {
        'email':forms.EmailInput(attrs={'class' : 'form-control'}),
        'username':forms.TextInput(attrs={'class' : 'form-control'}),
        'first_name':forms.TextInput(attrs={'class' : 'form-control'}),
        'last_name':forms.TextInput(attrs={'class' : 'form-control'}),
        }

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password2 = cleaned_data['comfirm_password']
        password1 = cleaned_data['password'] 

        if password1 != password2:
            raise ValidationError(_('password mismatched , enter same password in both field'))

        return cleaned_data


class ProfileForm(ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class' : 'form-control'}))
    
    class Meta:
        model  = Profile
        fields = ['username','first_name','last_name','email','gender','age','nationality','phone_no','description','photo','resume']
        widgets = {
        'country': CountrySelectWidget(attrs={'class' : 'form-control'}),
        'phone_no':forms.TextInput(attrs={'class' : 'form-control'}),
        'age':forms.NumberInput(attrs={'class' : 'form-control'}),
        'description':forms.Textarea(attrs={'class' : 'form-control'}),
        'gender': forms.Select(attrs={'class':'regDropDown form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        # Get 'initial' argument if any
        profile = kwargs.get('instance', None)
        updated_initial = {}
        updated_initial['username'] = profile.user.username
        updated_initial['first_name'] = profile.user.first_name
        updated_initial['last_name'] = profile.user.last_name
        updated_initial['email'] = profile.user.email   
        kwargs.update(initial=updated_initial)
        super(ProfileForm, self).__init__(*args, **kwargs)

class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = ['title','motivation','keywards','catagory','cover_photo']
        widgets = {
        'title':forms.TextInput(attrs={'class' : 'form-control'}),
        'motivation':forms.Textarea(attrs={'class' : 'form-control'}),
        'keywards':forms.Textarea(attrs={'class' : 'form-control'}),
        }

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['post_type','heading','description']
        widgets = {
        'heading':forms.TextInput(attrs={'class' : 'form-control'}),
        'description':forms.Textarea(attrs={'class' : 'form-control'})
        }


class LessonForm(ModelForm):
    lesson_video = forms.FileField(required=False);
    lesson_file = forms.FileField(required=False);


    class Meta:
        model = Lesson
        fields = ['topic','lesson_no','motivation','lesson_file','lesson_video']
        widgets = {
        'lesson_no':forms.NumberInput(attrs={'class' : 'form-control'}),
        'topic':forms.TextInput(attrs={'class' : 'form-control'}),
        'motivation':forms.Textarea(attrs={'class' : 'form-control'}),
        }


    


