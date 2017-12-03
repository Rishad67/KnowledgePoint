from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
# to get this field use-"pip install django-phonenumber-field"
from phonenumber_field.modelfields import PhoneNumberField 
# to get this field use-"pip install django-countries" 
from django_countries.fields import CountryField
# Create your models here.

class Profile(models.Model):

	GENDER=(('M','male'),('F','female'))
	
	user = models.OneToOneField(User,on_delete=models.CASCADE)
	description = models.TextField(max_length=300, help_text="Enter a brief description about profession or educational background")
	gender = models.CharField(max_length=1,choices=GENDER,blank=True)
	age = models.PositiveIntegerField(null=True,blank=True)
	nationality = CountryField(blank_label='select country')
	phone_no = PhoneNumberField(blank=True,default="+880")
	resume = models.FileField(upload_to='Profile',null=True,blank=True)
	photo = models.ImageField(upload_to='Profile',null=True,blank=True,width_field="width_field",height_field="height_field")
	height_field = models.IntegerField(default=0)
	width_field = models.IntegerField(default=0)



	def __str__(self):
	 	return self.user.username

	def get_absolute_url(self):
		return reverse('user_detail', args=[str(self.id)])

	class Meta:
	 	verbose_name = 'Profile'
	 	verbose_name_plural = 'Profiles'


class Course(models.Model):

	title = models.CharField(max_length=100)
	instructor = models.ForeignKey(User,on_delete=models.CASCADE)
	motivation = models.TextField(max_length=300, help_text="Enter a brief description about the course")
	keywards = models.TextField(max_length=200, help_text="Enter some keywards of course",null=True)
	rating = models.PositiveIntegerField(default=0)
	last_update = models.DateField(auto_now=True)
	active = models.BooleanField(default=False)
	cover_photo = models.ImageField(upload_to='Profile',null=True,blank=True,width_field="width_field",height_field="height_field")
	height_field = models.IntegerField(default=0)
	width_field = models.IntegerField(default=0)

	def __str__(self):
	 	return self.title

	def get_absolute_url(self):
		return reverse('course_detail', args=[str(self.id)])

	class Meta:
	 	verbose_name = 'Course'
	 	verbose_name_plural = 'Courses'
	 	permissions = (
            ('view_course_lessons', 'View course lessons'),
        )
	 		

class Lesson(models.Model):

	topic = models.CharField(max_length=100)
	course = models.ForeignKey(Course,on_delete=models.CASCADE)
	motivation = models.TextField(max_length=300, help_text="Enter a brief description about the lesson")
	lesson_no = models.PositiveIntegerField()
	lesson_file = models.FileField(upload_to='Course/lesson')
	lesson_video = models.FileField(upload_to='Course/lesson')




	def __str__(self):
	 	return self.topic

	def get_absolute_url(self):
		return reverse('lesson_detail', args=[str(self.id)])

	class Meta:
	 	verbose_name = 'Lesson'
	 	verbose_name_plural = 'Lessons'


class Registration(models.Model):
	student=models.ForeignKey(User,on_delete=models.CASCADE)
	course=models.ForeignKey(Course,on_delete=models.CASCADE)
	current_lesson=models.ForeignKey(Lesson,on_delete=models.CASCADE)


class Follow(models.Model):
	student=models.ForeignKey(User,on_delete=models.CASCADE)
	instructor=models.ForeignKey(Course,on_delete=models.CASCADE)