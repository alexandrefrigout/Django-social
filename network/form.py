from django import forms
from django.contrib.auth.models import User
from network.models import Profile
from registration.forms import RegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _

class UserRegistrationForm(RegistrationForm):

	class Meta:
		model = User
		fields = ("username", 
                  "email", 
                  "password1", 
                  "password2")

	username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class':'form-control'}))
	email = forms.EmailField(max_length=75, widget=forms.TextInput(attrs={'class':'form-control'}))
	password1 = forms.CharField(max_length=75, widget=forms.PasswordInput(attrs={'class':'form-control'}))
	password2 = forms.CharField(max_length=75, widget=forms.PasswordInput(attrs={'class':'form-control'}))

	Male = 'Homme'
	Female = 'Femme'

	GENDER_CHOICES = (
		(Male, 'Homme'),
		(Female, 'Femme'),
	)
	
	gender = forms.ChoiceField(label='Genre', widget=forms.Select(attrs={'class':'form-control'}), choices=GENDER_CHOICES)


	def clean(self):
		print self.cleaned_data
		password_undersized = _("Le mot de passe doit contenir au moins six caracteres.")
		super(UserRegistrationForm, self).clean()
		if len(self.cleaned_data['password1']) > 5:
			return self.cleaned_data
		else:
			print "mot de passe trop petit"
			raise forms.ValidationError(password_undersized)


		
	def save(self, commit=True):
		user = super(UserRegistrationForm, self).save(commit=True)    
		print "User saved"
		user.email = self.cleaned_data["email"]
		user.username = self.cleaned_data["username"]
		profile = Profile(
					systemuser=user, gender = self.cleaned_data["gender"])

		if self.commit:
			user.save()
			profile.save()

		return user

class UserLoginForm(AuthenticationForm):
	username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class':'form-control'}))
	password = forms.CharField(max_length=75, widget=forms.PasswordInput(attrs={'class':'form-control'}))

#class UserProfileForm(forms.ModelForm):
#	class Meta:
#		model = UserProfile
#		fields = ('gender')
