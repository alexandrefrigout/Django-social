from django import forms
from django.contrib.auth.models import User
from network.models import Profile
from network import customwidgets
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

	exclude = ['profilepicture', 'birthdate', 'country', 'city']

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


class UserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['username', 'email']

	username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class':'form-control'}))
	email = forms.EmailField(max_length=75, widget=forms.TextInput(attrs={'class':'form-control'}))


class ProfileForm(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		super(ProfileForm, self).__init__(*args, **kwargs)
		self.fields['birthdate'].required = False
		self.fields['profilepicture'].required = False


	class Meta:
		model = Profile
		fields = ['gender', 'birthdate', 'country', 'city', 'profilepicture']

	Male = 'Homme'
	Female = 'Femme'

	GENDER_CHOICES = (
		(Male, 'Homme'),
		(Female, 'Femme'),
	)

	birthdate = forms.DateField(('%d/%m/%Y',), widget=forms.DateTimeInput(format='%d/%m/%Y', attrs={'class':'form-control'}))
	profilepicture = forms.FileField(label='Photo de profil', widget=customwidgets.AdvancedFileInput(preview=None,attrs={}))
	gender = forms.ChoiceField(label='Genre', widget=forms.Select(attrs={'class':'form-control'}), choices=GENDER_CHOICES)
	city = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
	country = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))



