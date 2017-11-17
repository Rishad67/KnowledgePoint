from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
# to get this field use-"pip install django-phonenumber-field"
from phonenumber_field.modelfields import PhoneNumberField 
# to get this field use-"pip install django-countries" 
from django_countries.fields import CountryField
# Create your models here.

class Profile(models.Model):

	GENDER=(('M','male'),('F','female'))
	
	user = models.OneToOneField(User,on_delete=models.CASCADE)
	description = models.TextField(max_length=400, help_text="Enter a brief description about profession or educational background")
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



	 		