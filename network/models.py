from django.db import models
from django.contrib.auth.models import User
import datetime

class Profile(models.Model):

	Male = 'Homme'
	Female = 'Femme'

	GENDER_CHOICES = (
		(Male, 'Homme'),
		(Female, 'Femme'),
	)

	user = models.ForeignKey(User, unique=True, limit_choices_to={'is_staff': False})
	created = models.DateTimeField(auto_now_add=True)
	gender = models.CharField(max_length=15, choices=GENDER_CHOICES)


	def save(self, *args, **kwargs):
		#self.created = datetime.now()
		super(Profile, self).save(*args, **kwargs)


#class UserProfile(models.Model):
#	user = models.OneToOneField(User, unique=True)
#	Male = 'Homme'
#	Female = 'Femme'
#
#	GENDER_CHOICES = (
#		(Male, 'Homme'),
#		(Female, 'Femme'),
#	)
#	gender = models.CharField(max_length=15, choices=GENDER_CHOICES)
#
#	def __unicode__(self):
#		return self.user.username
#	
