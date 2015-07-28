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
	profilepicture = models.FileField(upload_to='pictures/%Y/%m/%d', null=True, blank=True)
	birthdate = models.DateField(null=True, blank=True)
	country = models.CharField(max_length=100)
	city = models.CharField(max_length=100)

	def __unicode__(self):
		return self.user.username


	def save(self, *args, **kwargs):
		super(Profile, self).save(*args, **kwargs)

        def follow(self, user):
                self.user.relationships.add(user)

        def unfollow(self, user):
                self.user.relationships.remove(user)

        def makeFriend(self, user):
                self.user.relationships.add(user, symmetrical=True)

