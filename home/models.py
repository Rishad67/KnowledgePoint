from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

# Create your models here.

class Profile(models.Model):

	user = models.OneToOneField(User,on_delete=models.CASCADE)
	description = models.TextField(max_length=200, help_text="Enter a brief description about profession or educational background")
	gender = models.CharField(max_length=1,choices=(('M','male'),('F','female')),blank=True)
	age = models.PositiveIntegerField(null=True,blank=True)
	nationality = models.CharField(max_length=10,blank=True)
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



	 		